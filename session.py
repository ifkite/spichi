# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: session.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-07-23 20:26:01
# =============================================================================
'''


# TODO: localization
from time import time
from threading import local
import redis
from utils import generate_key
import json



# TODO: 不同的backend, 比如redis, memory
class SessionStore(object):

    def get_or_create_session(self, sessionid):
        """
            return sessionid, dict_data, and timestamp
        """
        pass


class RedisSessionStore(SessionStore):
    #TODO: 可配置
    backend = redis.Redis(host='localhost', port=6379, db=0)
    prefix = 'spichi:sid'
    keys = ['expires', 'data']


    def get_or_create_session(self, sessionid):
        if sessionid is None:
            return self.create_session()

        session = self.get_session(sessionid)
        if not session:
            return self.create_session()
        else:
            return session

    @staticmethod
    def get_redis_key(sessionid):
        return '{0}:{1}'.format(RedisSessionStore.prefix, sessionid)

    def get_session(self, sessionid):
        #TODO: exception
        expires, data = RedisSessionStore.backend.hmget(name=RedisSessionStore.get_redis_key(sessionid), keys=RedisSessionStore.keys)
        # TODO
        return sessionid, json.loads(data), expires

    def create_session(self):
        sessionid = self.generate_sessionid()
        # TODO: set default expires
        expires = time() + 3600
        # TODO: exception
        RedisSessionStore.backend.hmset(RedisSessionStore.get_redis_key(sessionid), {'expires': expires, 'data': {}})
        return sessionid, {}, expires

    def save_session(self, sessionid, data, expires):
        # TODO
        RedisSessionStore.backend.hmset(RedisSessionStore.get_redis_key(sessionid), {'expires': expires, 'data': json.dumps(data)})

    def generate_sessionid(self):
        # TODO set salt
        return generate_key(salt='')


class SessionBase(object):
    #TODO: SessionStore的传参
    #TODO: 可配置不同的SessionStore
    store = RedisSessionStore()

    def __init__(self, sessionid):
        self.sessionid, self.data, self.expires = self.store.get_or_create_session(sessionid)

    def check_session(self):
        #TODO: 更本地化检查, 更多的检查
        if time() > self.expires:
            # TODO: raise 一个合适的异常
            raise Exception

    def save(self):
        self.store.save_session(self.sessionid, self.data, self.expires)


# TODO: 使用起来更方便, 当前使用方式
# from session import thread_local
# thread_local.session.data['hello'] = 'world'
# thread_local.session.data.get('hello')
thread_local = local()


class SessionHandler(object):
    _config = {'max_age': None, 'expires': None, 'path':'/', 'domain': None, 'secure': False, 'httponly': True}
    session_key = '_sessionid'

    def pre_process(self, request):
        sessionid = request.cookies.get(self.session_key)
        thread_local.session = SessionBase(sessionid)
        thread_local.session.check_session()

    def post_process(self, request, response):
        response.set_cookie(key=self.session_key, value=thread_local.session.sessionid, **self._config)
