#!/usr/bin/env python3
'''
0. Writing strings to Redis
'''
import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ to count how many times methods of the Cache class are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache():
    '''
    a Cache class.
    '''
    def __init__(self) -> None:
        '''
        In the __init__ method,
        store an instance of the Redis client as
        a private variable named
        _redis (using redis.Redis()) and flush
        the instance using flushdb.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        a store method that takes a data argument
        and returns a string. The method should generate
        a random key (e.g. using uuid), store the input
        data in Redis using the random key and return the key.
        Remember that data can be a str, bytes, int or float.
        '''
        userid = str(uuid4())
        self._redis.set(userid, data)
        return userid

    def get(self, key: str, fn: Optional[Callable] = None):
        '''
        a get method that take a key string argument and an
        optional Callable argument named fn.
        This callable will be used to convert the data back
        to the desired format.
        '''
        info = self._redis.get(key)
        return info if not fn else fn(info)

    def get_str(self, key: str) -> str:
        '''
        parametrize Cache.get with the correct conversion function
        '''
        r = self._redis.get(key)
        return r.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ automatically parametrize Cache.get to int """
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data


def replay(method: Callable):
    """ display the history of calls of a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))
    inputList = redis.lrange(inputs, 0, -1)
    outputList = redis.lrange(outputs, 0, -1)
    redis_zipped = list(zip(inputList, outputList))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
