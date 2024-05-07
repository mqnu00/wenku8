import pprint
import time

from cache.cache_type.basecache import BaseCache
from cachelib.serializers import SimpleSerializer
import typing as _t


class SimpleCache(BaseCache):
    serializer = SimpleSerializer()

    def __init__(
            self,
            threshold: int = 500,
            default_timeout: int = 300,
            enable_ttl: bool = True,
            refresh_type: str = 'FIFO',
            ignore_errors=False
    ):
        """

        :param threshold:
        :param default_timeout:
        :param enable_ttl: 是否使用缓存过期策略
        :param refresh_type: 使用什么缓存算法 FIFO LRU LFU
        """
        BaseCache.__init__(self, default_timeout)
        self._cache: _t.Dict[str, _t.Any] = {}
        self._threshold = threshold or 500
        self._enable_ttl = enable_ttl
        if refresh_type != 'FIFO' and refresh_type != 'LFU':
            raise ValueError('refresh_type must be "FIFO" or "LFU"')
        self._refresh_type = refresh_type
        pprint.pprint(self.__dict__)

    @classmethod
    def factory(cls, app, config, args, kwargs):
        kwargs.update(
            dict(
                threshold=config["CACHE_THRESHOLD"],
                ignore_errors=config["CACHE_IGNORE_ERRORS"],
                refresh_type=config["REFRESH_TYPE"],
                enable_ttl=config["ENABLE_TTL"]
            )
        )
        return cls(*args, **kwargs)

    def _show(self):
        pprint.pprint(self._cache)

    def _over_threshold(self) -> bool:
        return len(self._cache) > self._threshold

    def _remove_expired(self, now: float) -> None:
        """TTL

        :param now:
        :return:
        """
        to_remove: list = []
        if self._refresh_type == 'FIFO':
            to_remove = [k for k, (expires, _) in self._cache.items() if expires < now]
        elif self._refresh_type == 'LFU':
            to_remove = [k for k, (_f, expires, _v) in self._cache.items() if expires < now]
        for k in to_remove:
            self._cache.pop(k, None)

    def _remove_older(self) -> None:

        """FIFO

        :return:
        """
        k_ordered = (
            k for k, v in sorted(
            self._cache.items(), key=lambda item: item[1][0]
        )
        )

        for k in k_ordered:
            self._cache.pop(k, None)
            if not self._over_threshold():
                break

    def _remove_low_frequency(self) -> None:
        """LRU

        :return:
        """
        k_ordered = (
            k for k, v in sorted(
            self._cache.items(), key=lambda item: item[1][0]
        )
        )

        for k in k_ordered:
            self._cache.pop(k, None)
            if not self._over_threshold():
                break

    def _prune(self) -> None:
        if self._over_threshold() and self._enable_ttl:
            now = time.time()
            self._remove_expired(now)
        if self._over_threshold():
            if self._refresh_type == 'FIFO':
                self._remove_older()
            elif self._refresh_type == 'LFU':
                self._remove_low_frequency()

    def _normalize_timeout(self, timeout: _t.Optional[int]) -> int:
        timeout = BaseCache._normalize_timeout(self, timeout)
        if timeout > 0:
            timeout = int(time.time()) + timeout
        return timeout

    def set(self, key: str, value: _t.Any, timeout: _t.Optional[int] = None) -> _t.Optional[bool]:
        self._prune()
        if self._refresh_type == 'FIFO':
            expires = self._normalize_timeout(timeout)
            self._cache[key] = (expires, self.serializer.dumps(value))
        elif self._refresh_type == 'LFU':
            frequency = 0
            expires = self._normalize_timeout(timeout)
            self._cache[key] = (frequency, expires, self.serializer.dumps(value))
        return True

    def add(self, key: str, value: _t.Any, timeout: _t.Optional[int] = None) -> bool:
        self._prune()
        if key in self._cache.items():
            return False
        if self._refresh_type == 'FIFO':
            expires = self._normalize_timeout(timeout)
            item = (expires, self.serializer.dumps(value))
            self._cache.setdefault(key, item)
        elif self._refresh_type == 'LFU':
            expires = self._normalize_timeout(timeout)
            frequency = 0
            item = (frequency, expires, self.serializer.dumps(value))
            self._cache.setdefault(key, item)

    def get(self, key: str) -> _t.Any:
        try:
            if self._refresh_type == 'FIFO':
                expires, value = self._cache[key]
                return self.serializer.loads(value)
            elif self._refresh_type == 'LFU':
                frequency, _, value = self._cache[key]
                frequency = frequency + 1
                self._cache[key] = (frequency, _, value)
                return self.serializer.loads(value)
        except KeyError:
            return None

    def has(self, key: str) -> bool:
        try:
            self._prune()
            return key in self._cache.keys()
        except KeyError:
            return False

    def delete(self, key: str) -> bool:
        return self._cache.pop(key, None) is not None

    def clear(self) -> bool:
        self._cache.clear()
        return not bool(self._cache)

    def show(self):
        pprint.pprint(self._cache)


if __name__ == '__main__':
    test = SimpleCache(refresh_type='LFU', enable_ttl=False, threshold=3, default_timeout=5)
    while True:
        check = input("opt: ")
        if check == "1":
            test.show()
        elif check == "2":
            key = input("key: ")
            value = input("value: ")
            test.set(key, value)
        elif check == "3":
            key = input("key: ")
            print(test.get(key))
        else:
            break
