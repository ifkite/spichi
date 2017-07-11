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
def dispatch_response(request):
    return Response('hello')

def spichi(environ, start_response):
    request = Request(environ)
    response = dispatch_response(request)
    return response(environ, start_response)
