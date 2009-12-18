A sweet little cache panel for `django-debug-toolbar`_.  Displays all commands
and keys sent to the cache backend, and records timing.  Cache hits are shown in
green because they make us happy.  It's not very pretty right now.  Please help.

Installation
------------

Get it with your pip::

    pip install -e git://github.com/jbalogh/django-debug-cache-panel#egg=cache_panel

Then you need to add it to settings.py under ``DEBUG_TOOLBAR_PANELS``::

    DEBUG_TOOLBAR_PANELS = (
        '...',
        'cache_panel.CachePanel',
        '...',
    )

Since you may be using the default panel settings, here's what the whole thing
should look like::

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )

Put ``'cache_panel.CachePanel'`` in there somewhere.

This has been tested with ``locmem`` and very briefly with ``memcached``.  I
didn't see any problems.

.. _`django-debug-toolbar`: http://github.com/robhudson/django-debug-toolbar
