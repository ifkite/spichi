# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: spichi.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#    LastChange: 2017-07-14 08:42:53
# =============================================================================
'''
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from config import Config
import os
import re
import json

from session import SessionHandler
from cache import CacheFactory
from utils import UploadHanderFactory
from database import DataBaseFactory
from excepts import ExceptHandler, handle_except


class Spichi(object):

    url_map = Map([])
    view_func = {}
    pre_handler = [SessionHandler]
    post_hander = [SessionHandler]

    #TODO
    # set session, set databases and set uploader should be executed in spichi class

    def set_databases(self):
        self.databases = {
                db_name: DataBaseFactory(db_value['db_type']).build(db_value['db_conf'])
                for db_name, db_value in self.conf['DATABASES'].iteritems()
                }

    def set_session(self):
        SessionHandler.set_store(self.conf['SESSION_STORE']['name'], **self.conf['SESSION_STORE']['conf'])

    def set_cache(self):
        self.caches = {
                cache_name: CacheFactory(cache_name).build(**cache_value)
                for cache_name, cache_value in self.conf['CACHE'].iteritems()
                }

    def set_upload_handler_class(self):
        self.UploadHandlerClass = UploadHanderFactory(self.conf['UPLOAD_CLASS']).get_backend()

    def set_config(self, *args, **kwargs):
        default_path = os.path.dirname(os.path.abspath(__file__))
        conf_filepath = kwargs.get('path', default_path)
        conf_filename = kwargs.get('conf', 'develop.json')
        self.conf = Config(conf_filepath)

        if re.search('\.py', conf_filename):
            self.conf.from_pyfile(conf_filename)
        else:
            self.conf.from_json(conf_filename)

    def __init__(self, *args, **kwargs):
        self.set_config(*args, **kwargs)
        self.set_databases()
        self.set_session()
        self.set_cache()
        self.set_upload_handler_class()

    def route(self, rule, endpoint):
        def decorator(func):
            self.add_url(rule, endpoint, func)
        return decorator

    def route_class(self, rule, endpoint, *cls_args, **cls_kwargs):
        def decorator(cls):
            obj = cls(*cls_args, **cls_kwargs)
            self.add_url(rule, endpoint, obj)
            return cls
        return decorator

    def add_url(self, rule, endpoint, func):
        self.url_map.add(Rule(rule, endpoint=endpoint))
        self.view_func.update({endpoint: func})

    def pre_handle(self, request):
        for handler in self.pre_handler:
            handler().pre_process(request)

    def post_handle(self, request, response):
        for handler in self.post_hander:
            handler().post_process(request, response)

    def response_wrapper(self, endpoints, request, values):
        results = self.view_func[endpoints](request, **values) or []
        if isinstance(results, Response):
            return results
        return Response(json.dumps({'error_code': 200, 'error_msg': '', 'error_detail': '', 'results': results}), mimetype='application/json')


    def dispatch_response(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoints, values = adapter.match()
            return self.response_wrapper(endpoints=endpoints, request=request, values=values)
        except Exception as e:
            return handle_except(e, ExceptHandler)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        self.pre_handle(request)
        response = self.dispatch_response(request)
        self.post_handle(request, response)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(*args, **kwargs):
    return Spichi(*args, **kwargs)
