# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: database.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-10-03 10:20:13
# =============================================================================
'''


import six
import abc
import types
from sqlalchemy import create_engine as sql_create_engine
from sqlalchemy.exc import ResourceClosedError as SQLRescoureClosedError
from factory import GeneralFactory


class ResourceClosedError(SQLRescoureClosedError):
    '''
    '''


@six.add_metaclass(abc.ABCMeta)
class BaseDataHandler(object):

    def __init__(self, *args, **kwargs):
        self.set_engine(*args, **kwargs)
        self.connect()

    @abc.abstractmethod
    def set_engine(self):
        '''
        '''

    @abc.abstractmethod
    def connect(self):
        '''
        '''

    @abc.abstractmethod
    def execute(self):
        '''
        '''


class SQLDataHandler(BaseDataHandler):

    def set_engine(self, *args, **kwargs):
        if isinstance(self.engine, types.FunctionType):
            self.engine = sql_create_engine(*args, **kwargs)

    def connect(self):
        if isinstance(self.conn, types.FunctionType):
            self.conn = self.engine.connect()

    def execute(self, *args, **kwargs):
        try:
            return self.conn.execute(*args, **kwargs)
        except ResourceClosedError:
            self.connect()
            return self.conn.execute(*args, **kwargs)

    def __getattr__(self, name):
        '''
        act as a proxy
        '''
        def wrap(*args, **kwargs):
            return getattr(self.conn, name)(*args, **kwargs)

        return wrap


DataBaseFactory = GeneralFactory.gen()
DataBaseFactory.backend_dict = {'sql': SQLDataHandler}
