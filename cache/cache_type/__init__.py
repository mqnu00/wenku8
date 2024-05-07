from cache.cache_type.simplecache import SimpleCache

__all__ = (
    'simple'
)


def simple(app, config, args, kwargs):
    return SimpleCache.factory(app, config, args, kwargs)
