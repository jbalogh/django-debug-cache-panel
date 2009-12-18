#from distutils.core import setup
from setuptools import setup


setup(
    name='django-debug-cache-panel',
    version='0.0.1',
    description='Sweet little cache panel for django-debug-toolbar',
    long_description=open('README.rst').read(),
    author='Jeff Balogh',
    author_email='me@jeffbalogh.org',
    url='http://github.com/jbalogh/django-debug-cache-panel',
    license='BSD',
    py_modules=['cache_panel'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Ranking :: Fabulous',
    ]
)
