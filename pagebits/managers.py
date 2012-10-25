from django.db import models
from django.core.cache import cache
from django.conf import settings

from .utils import bitgroup_cache_key


class BitGroupManager(models.Manager):

    def get_group(self, slug):
        """ Retrieve a group by slug, with caching """
        key = bitgroup_cache_key(slug)
        cached_group = cache.get(key)

        if not cached_group:
            cached_group = self.get_query_set().select_related(
                'bits',
                'bits__data'
            ).get(slug=slug)

            timeout = getattr(settings, 'PAGEBITS_CACHE_TIMEOUT', 3600)

            cache.set(key, cached_group, int(timeout))

        return cached_group
