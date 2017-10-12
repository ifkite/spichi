# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: exceptions.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-08-06 15:24:48
# =============================================================================
'''


import json

class SpichiExcept(Exception):

    status_code = 500
    error_msg = 'Internal Server Error'


class InternalServerExcept(SpichiExcept):
    pass


class BadRequestExcept(SpichiExcept):

    status_code = 400
    error_msg = 'Bad Request'


class UnauthorizedExcept(SpichiExcept):

    status_code = 401
    error_msg = 'Unauthorized'


class PaymentRequiredExcept(SpichiExcept):

    status_code = 402
    error_msg = 'Payment Required'


class ForbiddenExcept(SpichiExcept):

    status_code = 403
    error_msg = 'Forbidden'


class NotFoundExcept(SpichiExcept):

    status_code = 404
    error_msg = ' Not Found'


class MethodNotAllowedExcept(SpichiExcept):

    status_code = 405
    error_msg = 'Method Not Allowed'


class NotAcceptableExcept(SpichiExcept):

    status_code = 406
    error_msg = 'Not Acceptable'


class RequestTimeoutExcept(SpichiExcept):

    status_code = 408
    error_msg = 'Request Timeout'


class GoneExcept(SpichiExcept):

    status_code = 410
    error_msg = 'Gone'


class ExceptHandler(object):

    def __init__(self, e):
        from werkzeug.wrappers import Response

        status = getattr(e, 'status_code', 400)
        err_content = self.set_content(e)
        self.response = Response(err_content, status=status, mimetype='application/json')

    def set_content(self, e):
        error_msg = getattr(e, 'error_msg', '')
        error_detail = getattr(e, 'message', '')
        error_code = getattr(e, 'error_code', 400)
        return json.dumps({
                    "error_code": error_code,
                    "error_msg": error_msg,
                    "error_detail": error_detail,
                    "results": []
                })


def handle_except(e, handler):
    return handler(e).response
