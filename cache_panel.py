import time

from django.core import cache
from django.template import Template, Context
from django.utils.translation import ugettext as _

from debug_toolbar.panels import DebugPanel


class CachePanel(DebugPanel):

    name = 'Cache'
    has_content = True

    def nav_title(self):
        return _('Cache')

    def title(self):
        return _('Cache Queries')

    def nav_subtitle(self):
        # Aggregate stats.
        stats = {'hit': 0, 'miss': 0, 'time': 0}
        for log in wrapper.log:
            if hasattr(log, 'hit'):
                stats[log.hit and 'hit' or 'miss'] += 1
            stats['time'] += log.time

        # No ngettext, too many combos!
        stats['time'] = round(stats['time'], 2)
        return _('%(hit)s hits, %(miss)s misses in %(time)sms') % stats

    def content(self):
        context = {'logs': wrapper.log}
        return Template(template).render(Context(context))

    def url(self):
        return ''

    def process_request(self, request):
        wrapper.reset()


class CacheLog(object):

    def __init__(self, name, key):
        self.name = name
        self.key = key


def logged(f):
    name = f.__name__
    def wrapper(self, key, *args, **kwargs):
        # Store the log here so the wrapper functions can update it.
        self.log.append(CacheLog(name, key))
        t = time.time()

        val = f(self, key, *args, **kwargs)

        self.log[-1].time = 1000 * (time.time() - t)
        return val

    return wrapper


class CacheWrapper(object):
    """Subclass of the current cache backend."""

    def __init__(self, cache):
        # These are the methods we're going to replace.
        methods = 'add clear get set delete get_many'.split()

        # Store copies of the true methods.
        self.real_methods = dict((m, getattr(cache, m)) for m in methods)

        # Hijack the cache object.
        for method in methods:
            setattr(cache, method, getattr(self, method))

        self.reset()

    def reset(self):
        self.log = []

    @logged
    def add(self, key, value, timeout=None):
        return self.real_methods['add'](key, value, timeout)

    @logged
    def get(self, key, default=None):
        val = self.real_methods['get'](key, default)
        self.log[-1].hit = val != default
        return val

    @logged
    def set(self, key, value, timeout=None):
        return self.real_methods['set'](key, value, timeout)

    @logged
    def delete(self, key):
        return self.real_methods['delete'](key)

    @logged
    def get_many(self, keys):
        val = self.real_methods['get_many'](keys)
        self.log[-1].hit = bool(val)
        return val

    def clear(self):
        return self.real_methods['clear']()


wrapper = CacheWrapper(cache.cache)
cache.cache = wrapper


template = """
<style type="text/css">
  #djDebugCacheTable tr.hit.djDebugOdd { background-color: #d7f3bc; }
  #djDebugCacheTable tr.hit.djDebugEven { background-color: #c7fcd3; }
</style>
<table id="djDebugCacheTable">
  <thead>
    <tr>
      <th>{{ _('Time (ms)') }}</th>
      <th>{{ _('Method') }}</th>
      <th>{{ _('Key') }}</th>
    </tr>
  </thead>
  <tbody>
    {% for log in logs %}
      {% if log.hit %}
      <tr class="hit {% cycle 'djDebugOdd' 'djDebugEven' %}">
      {% else %}
      <tr class="{% cycle 'djDebugOdd' 'djDebugEven' %}">
      {% endif %}
        <td>{{ log.time|floatformat:"2" }}</td>
        <td class="{{ log.name }} method">{{ log.name }}</td>
        <td>{{ log.key }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
"""
