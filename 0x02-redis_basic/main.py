#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

'''
cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))
'''

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value


def get_str(self, key) -> str:
    '''
    parametrize Cache.get with the correct conversion function
    '''
    n = self.get(key, str)
    return n


def get_int(self, key) -> int:
    '''parametrize Cache.get with the correct conversion function
    '''
    ret = self.get(key, int)
    return ret
