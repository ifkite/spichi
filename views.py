# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: views.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-07-16 12:06:42
# =============================================================================
'''
from werkzeug.exceptions import HTTPException


class View(object):

    def dispatch(self, request, *args, **kwargs):
        request_http_method = request.method.lower()
        view_func = getattr(self, request_http_method, None)
        if view_func:
            return view_func(request, *args, **kwargs)
        else:
            raise HTTPException

    def __call__(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)
