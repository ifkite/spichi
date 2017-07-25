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


# TODO: 不同的backend, 比如redis, memory
class SessionStore(object):

    def get_or_create_session(self, sessionid):
        """
            return session_value, dict_data, and timestamp
        """
        pass


class SessionBase(object):
    #TODO: SessionStore的传参
    #TODO: 可配置不同的SessionStore
    store = SessionStore()

    def __init__(self, sessionid):
        self.value, self.data, self.expires = self.store.get_or_create_session(sessionid)

    def check_session(self):
        #TODO: 更本地化检查, 更多的检查
        if time() > self.expires:
            # TODO: raise 一个合适的异常
            raise Exception


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
        response.set_cookie(key=self.session_key, value=thread_local.session.value, **self._config)
