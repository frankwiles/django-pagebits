from django.conf import settings


def bitgroup_cache_key(slug):
    return "%s:%s" % (
        getattr(settings, 'PAGEBIT_CACHE_PREFIX', 'pagebits'),
        slug
    )

