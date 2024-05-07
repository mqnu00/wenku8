import functools
import pprint
import warnings

from flask import request, Flask, current_app
from typing import Callable, Union, Any
import typing as _t

from cache.cache_type.basecache import BaseCache
from cache.cache_type.simplecache import SimpleCache
from cache.cache_type.utils import import_string


class Cache:

    def __init__(
            self,
            app: _t.Optional[Flask] = None,
            config: _t.Optional[_t.Dict] = None
    ) -> None:

        self.config = config
        self.source_check = None

        if app is not None:
            self.init_app(app, config)

        self.data = dict()
        self.app = app

    def init_app(self, app: Flask, config: _t.Optional[_t.Dict]) -> None:
        """给 Flask 实例初始化缓存，这会将缓存和 Flask 示例绑定在一起

        :param app:
        :param config:
        :return:
        """

        base_config = app.config.copy()
        if self.config:
            base_config.update(self.config)
        if config:
            base_config.update(config)
        config = base_config

        config.setdefault("CACHE_DEFAULT_TIMEOUT", 300)
        config.setdefault("CACHE_IGNORE_ERRORS", False)
        config.setdefault("CACHE_THRESHOLD", 500)
        config.setdefault("CACHE_KEY_PREFIX", "flask_cache_")
        config.setdefault("CACHE_MEMCACHED_SERVERS", None)
        config.setdefault("CACHE_DIR", None)
        config.setdefault("CACHE_OPTIONS", None)
        config.setdefault("CACHE_ARGS", [])
        config.setdefault("CACHE_TYPE", "null")
        config.setdefault("CACHE_NO_NULL_WARNING", False)
        config.setdefault("CACHE_SOURCE_CHECK", False)
        # design
        config.setdefault("REFRESH_TYPE", 'FIFO')
        config.setdefault("ENABLE_TTL", True)

        if config["CACHE_TYPE"] == "null" and not config["CACHE_NO_NULL_WARNING"]:
            warnings.warn(
                "cache_init: CACHE_TYPE is set to null, "
                "caching is effectively disabled."
            )

        if (
                config["CACHE_TYPE"] in ["filesystem", "FileSystemCache"]
                and config["CACHE_DIR"] is None
        ):
            warnings.warn(
                f"cache_init: CACHE_TYPE is set to {config['CACHE_TYPE']} but no "
                "CACHE_DIR is set."
            )

        self.source_check = config["CACHE_SOURCE_CHECK"]
        self._set_cache(app, config)

    def _set_cache(self, app: Flask, config: _t.Dict) -> None:
        import_me = config["CACHE_TYPE"]
        plain_name_used: bool = True
        if "." not in import_me:
            plain_name_used = True
            import_me = "cache.cache_type." + import_me
        else:
            plain_name_used = False

        cache_factory = import_string(import_me)
        cache_args = config["CACHE_ARGS"][:]
        cache_options = {"default_timeout": config["CACHE_DEFAULT_TIMEOUT"]}

        if isinstance(cache_factory, type) and issubclass(cache_factory, BaseCache):
            cache_factory = cache_factory.factory
        elif plain_name_used:
            warnings.warn(
                "Using the initialization functions in flask_caching.backend "
                "is deprecated.  Use the a full path to backend classes "
                "directly.",
                category=DeprecationWarning,
            )

        if config["CACHE_OPTIONS"]:
            cache_options.update(config["CACHE_OPTIONS"])

        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions.setdefault("cache", {})
        app.extensions["cache"][self] = cache_factory(
            app, config, cache_args, cache_options
        )
        self.app = app

    def _call_fn(self, fn, *args, **kwargs):
        ensure_sync = getattr(self.app, "ensure_sync", None)
        if ensure_sync is not None:
            return ensure_sync(fn)(*args, **kwargs)
        return fn(*args, **kwargs)

    @property
    def cache(self) -> SimpleCache:
        app = current_app or self.app
        return app.extensions["cache"][self]

    def cached(
            self,
            threshold: int = 5,
            timeout: _t.Optional[int] = None,
            key_redo: Union[str, int] = None,
    ) -> Callable:
        def decorator(f: Callable) -> Callable:
            @functools.wraps(f)
            def wrapper(*argc, **kwargs):
                if key_redo is None:
                    key = 'flask_cache_' + request.path
                else:
                    key = 'flask_cache_' + key_redo
                value = self.get(key)
                if value is None:
                    value = f(*argc, **kwargs)
                    self.set(key, value)
                return value
            return wrapper

        return decorator

    def get(self, *args, **kwargs) -> Any:
        """Proxy function for internal cache object."""
        return self.cache.get(*args, **kwargs)

    def has(self, *args, **kwargs) -> bool:
        """Proxy function for internal cache object."""
        return self.cache.has(*args, **kwargs)

    def set(self, *args, **kwargs) -> _t.Optional[bool]:
        """Proxy function for internal cache object."""
        return self.cache.set(*args, **kwargs)

    def add(self, *args, **kwargs) -> bool:
        """Proxy function for internal cache object."""
        return self.cache.add(*args, **kwargs)

    def delete(self, *args, **kwargs) -> bool:
        """Proxy function for internal cache object."""
        return self.cache.delete(*args, **kwargs)

    def clear(self) -> bool:
        """Proxy function for internal cache object."""
        return self.cache.clear()
