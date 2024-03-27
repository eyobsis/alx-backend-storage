#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """Decorator function to track and cache HTTP requests."""
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Wrapper function that:
        - checks whether a URL's data is cached
        - tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """Makes an HTTP request to a given endpoint."""
    response = requests.get(url)
    return response.text
