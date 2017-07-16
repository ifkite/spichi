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
from werkzeug.exceptions import HTTPException
# from utils import get_path_info


class Spichi(object):

    url_map = Map([])
    view_func = {}

    def __init__(self, *args, **kwargs):
        pass

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

    def dispatch_response(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoints, values = adapter.match()
            return Response(self.view_func[endpoints](request, **values))
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_response(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(*args, **kwargs):
    return Spichi(*args, **kwargs)
