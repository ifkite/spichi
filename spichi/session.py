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
import abc
import six
import redis
from utils import generate_key
import json
from factory import GeneralFactory


# TODO: 不同的backend, 比如redis, memory
@six.add_metaclass(abc.ABCMeta)
class SessionStore(object):

    def __init__(self, *args, **kwargs):
        self.config(*args, **kwargs)

    @abc.abstractmethod
    def config(self, *args, **kwargs):
        """
            config SessionStore backend
        """

    def get_or_create_session(self, sessionid):
        """
            return sessionid, dict_data, and timestamp
        """
        if sessionid is None:
            return self.create_session()

        session = self.get_session(sessionid)
        if not session:
            return self.create_session()
        else:
            return session

    @abc.abstractmethod
    def save_session(self, sessionid, data, expires):
        """
            save session data
        """


class RedisSessionStore(SessionStore):
    conf = {'host': '127.0.0.1', 'port': 6379, 'db': 1}
    prefix = 'spichi:sid'
    keys = ['expires', 'data']

    def config(self, *args, **kwargs):
        self.conf.update(**kwargs)
        self.backend = redis.Redis(host=self.conf.get('host'), port=self.conf.get('port'), db=self.conf.get('db'))


    @staticmethod
    def get_redis_key(sessionid):
        return '{0}:{1}'.format(RedisSessionStore.prefix, sessionid)

    def get_session(self, sessionid):
        #TODO: exception
        expires, data = self.backend.hmget(name=RedisSessionStore.get_redis_key(sessionid), keys=RedisSessionStore.keys)
        # TODO
        return sessionid, json.loads(data), expires

    def create_session(self):
        sessionid = self.generate_sessionid()
        # TODO: set default expires
        expires = time() + 3600
        # TODO: exception
        self.backend.hmset(RedisSessionStore.get_redis_key(sessionid), {'expires': expires, 'data': {}})
        return sessionid, {}, expires

    def save_session(self, sessionid, data, expires):
        # TODO
        self.backend.hmset(RedisSessionStore.get_redis_key(sessionid), {'expires': expires, 'data': json.dumps(data)})

    def generate_sessionid(self):
        # TODO set salt
        return generate_key(salt='')


class LocalSessionStore(SessionStore):
    sesseion_store = {}

    def config(self, *args, **kwargs):
        pass

    def get_session(self, sessionid):
        session_data = LocalSessionStore.sesseion_store.get(sessionid, {'expires': time(), 'data': {}})
        return sessionid, session_data.get('data'), session_data.get('expires')

    def create_session(self):
        sessionid = self.generate_sessionid()
        expires = time() + 3600
        LocalSessionStore.sesseion_store.update({sessionid: {'expires': expires, 'data': {}}})
        return sessionid, {}, expires

    def save_session(self, sessionid, data, expires):
        LocalSessionStore.sesseion_store.update({sessionid: {'expires': expires, 'data': data}})

    def generate_sessionid(self):
        # TODO set salt
        return generate_key(salt='')


SessionStoreFactory = GeneralFactory.gen()
SessionStoreFactory.backend_dict = {'redis': RedisSessionStore, 'local': LocalSessionStore}


class SessionBase(object):
    #TODO: SessionStore的传参

    @classmethod
    def set_store(cls, store_name, **conf):
        cls.store = SessionStoreFactory(store_name).build(**conf)

    def __init__(self, sessionid):
        self.sessionid, self.data, self.expires = self.store.get_or_create_session(sessionid)

    def check_session(self):
        #TODO: 更本地化检查, 更多的检查
        if time() > self.expires:
            # TODO: raise 一个合适的异常
            raise Exception

    def save(self):
        self.store.save_session(self.sessionid, self.data, self.expires)


# sample
# from session import session
# get session: session['count']
# set session: session['name'] = 'ifkite'
# save session: session.save()

class Session(dict):
    thread_local = local()

    def __getitem__(self, name):
        return Session.thread_local.session.data.get(name)

    def __setitem__(self, name, val):
        Session.thread_local.session.data[name] = val

    def save(self):
        Session.thread_local.session.save()


session = Session()
thread_local = Session.thread_local


class SessionHandler(object):
    _config = {'max_age': None, 'expires': None, 'path':'/', 'domain': None, 'secure': False, 'httponly': True}
    session_key = '_sessionid'

    @staticmethod
    def set_store(name, **conf):
        SessionBase.set_store(name, **conf)

    def pre_process(self, request):
        sessionid = request.cookies.get(self.session_key)
        thread_local.session = SessionBase(sessionid)
        thread_local.session.check_session()

    def post_process(self, request, response):
        response.set_cookie(key=self.session_key, value=thread_local.session.sessionid, **self._config)
