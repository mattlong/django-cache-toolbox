"""
Core methods
------------

.. autofunction:: cache_toolbox.core.get_instance
.. autofunction:: cache_toolbox.core.delete_instance
.. autofunction:: cache_toolbox.core.instance_key

"""

from django.core.cache import cache
from django.db import DEFAULT_DB_ALIAS

from . import app_settings

def cache_instance(instance, key=None, timeout=None):
    key = key or instance_key(model, instance_or_pk)
    data = create_cache_version(instance)

    if timeout is None:
        timeout = app_settings.CACHE_TOOLBOX_DEFAULT_TIMEOUT

    cache.set(key, data, timeout)

def create_cache_version(instance):
    data = {}
    for field in instance._meta.fields:
        # Harmless to save, but saves space in the dictionary - we already know
        # the primary key when we lookup
        if field.primary_key:
            continue
        if field.get_internal_type() == 'FileField':
            # Avoid problems with serializing FileFields
            # by only serializing the file name
            file = getattr(instance, field.attname)
            data[field.attname] = file.name
        else:
            data[field.attname] = getattr(instance, field.attname)

    return data

def get_instance(model, instance_or_pk, timeout=None, using=None):
    """
    Returns the ``model`` instance with a primary key of ``instance_or_pk``.

    If the data is cached it will be returned from there, otherwise the regular
    Django ORM is queried for this instance and the data stored in the cache.

    If omitted, the timeout value defaults to
    ``settings.CACHE_TOOLBOX_DEFAULT_TIMEOUT`` instead of 0 (zero).

    Example::

        >>> get_instance(User, 1) # Cache miss
        <User: lamby>
        >>> get_instance(User, 1) # Cache hit
        <User: lamby>
        >>> User.objects.get(pk=1) == get_instance(User, 1)
        True
    """

    pk = getattr(instance_or_pk, 'pk', instance_or_pk)
    key = instance_key(model, instance_or_pk)
    data = cache.get(key)

    if data is not None:
        try:
            # Try and construct instance from dictionary
            instance = model(pk=pk, **data)

            # Ensure instance knows that it already exists in the database,
            # otherwise we will fail any uniqueness checks when saving the
            # instance.
            instance._state.adding = False

            # Specify database so that instance is setup correctly. We don't
            # namespace cached objects by their origin database, however.
            instance._state.db = using or DEFAULT_DB_ALIAS

            return instance
        except:
            # Error when deserialising - remove from the cache; we will
            # fallback and return the underlying instance
            cache.delete(key)

    # Use the default manager so we are never filtered by a .get_query_set()
    instance = model._default_manager.using(using).get(pk=pk)

    cache_instance(instance, key=key, timeout=timeout)

    return instance

def update_instance(model, *instance_or_pk):
    """
    Updates/adds cache entries for the instance of this model
    and purges the cache keys for any primary keys passed
    """

    to_cache = {}
    to_delete = []

    for obj in instance_or_pk:
        key = instance_key(model, obj)
        pk = getattr(obj, 'pk', None)
        if pk: #obj is an instance, update its cache entry
            to_cache[key] = create_cache_version(obj)
        else: #obj is a pk, so just delete it
            to_delete.append(key)

    timeout = app_settings.CACHE_TOOLBOX_DEFAULT_TIMEOUT

    if to_cache:
        cache.set_many(to_cache, timeout)

    if to_delete:
        cache.delete_many(to_delete)

def delete_instance(model, *instance_or_pk):
    """
    Purges the cache keys for the instances of this model.
    """

    cache.delete_many([instance_key(model, x) for x in instance_or_pk])

def instance_key(model, instance_or_pk):
    """
    Returns the cache key for this (model, instance) pair.
    """

    return '%s.%s:%s' % (
        model._meta.app_label,
        model._meta.module_name,
        getattr(instance_or_pk, 'pk', instance_or_pk),
    )
