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
from time import time
try:
    import cPickle as pickle
except:
    import pickle


class CacheValue(object):
    from werkzeug.wrappers import Response as response
    support_type = (int, basestring, dict, list, tuple, response)

    @classmethod
    def serialize(cls, data):
        for t in cls.support_type:
            if isinstance(data, t):
                return pickle.dumps(data)

        raise Exception


    @classmethod
    def unserialize(cls, data):
        # shuold handle exception when called this func
        return pickle.loads(data)


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


    # sample
    # app = create_app()
    # cache = app.caches['redis'].cache
    #
    # @app.route('/', 'home')
    # @cache(10, 'home_result')
    # def home(request):
    #     return 'welcome to my home'
    #
    # @app.route_class('/hello', 'hello')
    # class Hello(View):
    #
    # @cache(10, 'hello')
    # def get(self, request):
    #     return 'hello world'
    #
    # NOTICE
    # cache function ONLY take effect when
    # the decorated function returns a string value

    def cache(self, expires, key):
        def decorator(func):
            def dict2str(d):
                return ':'.join(['{0}:{1}'.format(k, str(v)) for k,v in d.iteritems()])

            def make_real_key(k, kw):
                key_second_part = dict2str(kw)
                if key_second_part:
                    return '{0}:{1}'.format(k, key_second_part)
                else:
                    return k

            def wrapper(*args, **kwargs):
                try:
                    real_key = make_real_key(key, kwargs)
                except:
                    return func(*args, **kwargs)

                cache_val = self.get(real_key)
                if cache_val:
                    return CacheValue.unserialize(cache_val)

                result = func(*args, **kwargs)
                try:
                    result_serialized = CacheValue.serialize(result)
                    self.set(real_key, result_serialized, expires)
                except:
                    pass

                return result
            return wrapper
        return decorator


class LocalCache(BaseCache):
    _cache = {}

    def config(self, *args, **kwargs):
        pass

    def get(self, cache_key):
        _cache_key = self.make_key(cache_key)
        cache_result = self._cache.get(_cache_key)
        if not cache_result:
            return cache_result
        if cache_result and cache_result.get('expires') < time():
            cache_result = None
            self.delete(cache_key)
        return cache_result.get('value')

    def set(self, cache_key, cache_val, expires=None):
        _cache_key = self.make_key(cache_key)
        self._cache.update({
            _cache_key: {
                "value": cache_val,
                "expires": time() + expires
                }
            })

    def delete(self, cache_key):
        _cache_key = self.make_key(cache_key)
        try:
            return self._cache.pop(_cache_key)
        except KeyError:
            return None


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
CacheFactory.backend_dict = {'redis': RedisCache, 'local': LocalCache}
