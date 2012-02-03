# django-cache-toolbox-modified

Forked from <https://github.com/playfire/django-cache-toolbox>.

### Why did I fork?#

* I have several modifications regarding their cache invalidation policy that I want to experiment with.

* I contacted the author asking that they publish the project to PyPI for ease of installation and never heard back. As such, I am managing the modified version on PyPI.

### Modifications from django-cache-toolbox

Package available from PyPI: <http://pypi.python.org/pypi/django-cache-toolbox-modified/>. Can be installed by doing:

    pip install django-cache-toolbox-modified

The `aggressive_caching` flag can optionally be set when calling the `cache_model` function.  When set to True (by default, it is False), cache entries will updated rather than deleted when an instance is saved or updated.
