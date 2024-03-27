#!/usr/bin/env python3
""" Redis client module """
import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union

def count_calls(method: Callable) -> Callable:
    """Decorator to track call count of Cache class methods."""
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """Wrapper function to increment call count before executing the method."""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to track method arguments and outputs."""
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """Wrapper function to store method inputs and outputs."""
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper

def replay(fn: Callable) -> None:
    """Retrieve and display call history for a function."""
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')

class Cache:
    """Caching class"""
    def __init__(self) -> None:
        """Initialize a new cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with randomly generated key"""
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Retrieve value from Redis and optionally apply conversion function"""
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """Convert bytes to string"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """Convert bytes to integer"""
        return int(data)
