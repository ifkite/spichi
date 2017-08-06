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


class SpichiExcept(Exception):

    error_code = 500
    error_msg = 'Internal Server Error'


class InternalServerExcept(SpichiExcept):
    pass


class BadRequestExcept(SpichiExcept):

    error_code = 400
    error_msg = 'Bad Request'


class UnauthorizedExcept(SpichiExcept):

    error_code = 401
    error_msg = 'Unauthorized'


class PaymentRequiredExcept(SpichiExcept):

    error_code = 402
    error_msg = 'Payment Required'


class ForbiddenExcept(SpichiExcept):

    error_code = 403
    error_msg = 'Forbidden'


class NotFoundExcept(SpichiExcept):

    error_code = 404
    error_msg = ' Not Found'


class MethodNotAllowedExcept(SpichiExcept):

    error_code = 405
    error_msg = 'Method Not Allowed'


class NotAcceptableExcept(SpichiExcept):

    error_code = 406
    error_msg = 'Not Acceptable'


class RequestTimeoutExcept(SpichiExcept):

    error_code = 408
    error_msg = 'Request Timeout'


class GoneExcept(SpichiExcept):

    error_code = 410
    error_msg = 'Gone'
