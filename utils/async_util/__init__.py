import functools
import pickle
import pprint
import time
import typing as _t

import redis
import threadpool
from threadpool import ThreadPool
from redis import ConnectionPool, Redis


class AsyncUtil:

    def __init__(
            self,
            redis_conf: dict,
            num_workers: _t.Any
    ):
        self.redis_pool = ConnectionPool(host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db'])
        self.executor = ThreadPool(num_workers)

    def task_async(self):
        def new_thread(
                key: str,
                fn: _t.Callable,
                redis_client: Redis,
                args,
                kwargs
        ):
            """

            :param key:
            :param fn: 生成器，第一次先返回生成个数，接下来返回生成值
            :param redis_client:
            :param args:
            :param kwargs:
            :return:
            """
            value = self.check_task(key)
            if value:
                return
            itr = fn(*args, **kwargs)
            res = {
                "status": False,
                "time": int(0),
                "total": next(itr),
                "current": 0,
                "value": []
            }
            for i in itr:
                res["current"] = res["current"] + 1
                res["value"].append(i)
                res["time"] = int(time.time())
                value = pickle.dumps(res)
                redis_client.set(key, value)
            res["status"] = True
            value = pickle.dumps(res)
            redis_client.set(key, value)

        def decorator(fn: _t.Callable):
            def wrapper(*args, **kwargs):
                key = fn.__name__ + '_' + '_'.join([str(i) for i in args])
                self.executor.putRequest(threadpool.WorkRequest(new_thread,
                                                                args=[key, fn, Redis(connection_pool=self.redis_pool),
                                                                      args, kwargs]))
                self.executor.poll()
                return key

            return wrapper

        return decorator

    def check_task(self, key):
        redis_client = redis.Redis(connection_pool=self.redis_pool)
        value = redis_client.get(key)
        if value is None:
            return False
        value = pickle.loads(value)
        return value


if __name__ == '__main__':
    print(time.time())
    pass
    a = AsyncUtil(
        {
            'host': '127.0.0.1',
            'port': 6379,
            'db': 0
        },
        10
    )


    @a.task_async()
    def func(bbb):
        print(bbb)
        yield 5
        for i in range(5):
            time.sleep(1)
            yield i


    res = func(100)
    pass
    while True:
        time.sleep(2)
        value = a.check_task(res)
        print(value['current'], value['total'])
        if value['status']:
            break