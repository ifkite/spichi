# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: app.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#    LastChange: 2017-06-24 11:34:24
# =============================================================================
'''
from werkzeug.wrappers import Request, Response
# from utils import get_path_info


class Spichi(object):
    def __init__(self, *args, **kwargs):
        pass

    def dispatch_response(self, request):
        return Response('hello')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_response(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(*args, **kwargs):
    return Spichi(*args, **kwargs)
