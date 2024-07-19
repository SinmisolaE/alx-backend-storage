#!/usr/bin/env python3

""" Working with reddis using python """


import reddis
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ decorator that takes a single method
        Callable argument and returns a Callable
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrap the decorated func and return the wrapper """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ decorator to store the history of inputs
        and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrap the decorated function and return the wrapper """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    '''display the history of calls of a particular function.'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    """ Class performs operation with reddis """

    def __init__(self):
        """ constructor method"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[float, str, int, bytes]) -> str:
        """ generate a random key, store the input
            data in Redis using the random key and return the key.
        """

        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get_str(self, key: str) -> str:
        """ parametrize Cache.get with correct conversion function """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ parametrize Cache.get with correct conversion function """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
