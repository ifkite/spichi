# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: cache.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-09-24 11:40:27
# =============================================================================
'''


import redis
from factory import GeneralFactory


class BaseCache(object):
    cache_prefix = 'cache'

    def __init__(self, *args, **kwargs):
        self.config(*args, **kwargs)

    def make_key(self, cache_key):
        if isinstance(cache_key, basestring):
            return '{0}:{1}'.format(self.cache_prefix, cache_key)
        else:
            raise Exception('cache key is not a string')

    def config(self, *args, **kwargs):
        pass

    def get(self, cache_key):
        pass

    def set(self, cache_key, cache_val, expires=None):
        pass

    def delete(self, cache_key):
        pass

    def cache(self, expires, key):
        def decorator(func):
            def wrapper(*args, **kwargs):
                cache_val = self.get(key)
                if cache_val:
                    return cache_val
                result = func(*args, **kwargs)
                if isinstance(result, basestring):
                    self.set(key, result, expires)
                return result
            return wrapper
        return decorator


class RedisCache(BaseCache):
    conf = {'host': '127.0.0.1', 'port': 6379, 'db': 0}

    def config(self, *args, **kwargs):
        self.conf.update(kwargs)
        self._cache = redis.Redis(host=self.conf.get('host'), port=self.conf.get('port'), db=self.conf.get('db'))

    def get(self, cache_key):
        _cache_key = self.make_key(cache_key)
        return self._cache.get(_cache_key)

    def set(self, cache_key, cache_val, expires=None):
        _cache_key = self.make_key(cache_key)
        return self._cache.set(_cache_key, cache_val, expires)

    def delete(self, cache_key):
        _cache_key = self.make_key(cache_key)
        return self._cache.delete(_cache_key)


CacheFactory = GeneralFactory.gen()
CacheFactory.backend_dict = {'redis': RedisCache}
