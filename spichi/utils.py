# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: utils.py
#          Desc: 
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-06-27 07:22:02
# =============================================================================
'''
from hashlib import sha1
from random import random
from time import time
from os import path
from factory import GeneralFactory


def get_path_info(environ):
    from urllib import quote
    path_info = quote(environ.get('PATH_INFO',''),safe='/;=,')
    if not environ.get('SCRIPT_NAME'):
        return path_info[1:]
    else:
        return path_info


def time_text():
    return str(time()).encode('ascii')


def random_text():
    # PY2
    return unicode(random()).encode('ascii')


def generate_key(salt=None):
    return sha1(b''.join([
        salt,
        time_text(),
        random_text(),
        ])).hexdigest()


def redirect(location, status=302):
    """
    which is seldom used in api server
    """
    from werkzeug.wrappers import Response
    from werkzeug.urls import iri_to_uri
    location = iri_to_uri(location, safe_conversion=True)
    return Response(
            "<!DOCTYPE html>\
                <html>\
                    <h1>Redirecting...</h1>\
                    <a href='{0}'>touch this to make manually redirection</a>\
                </html>"
            .format(location), status=status, headers={'Location': location})


# sample
# app = create_app()
# @app.route('/', 'home')
# def home(request):
#   app.UploadHandlerClass(request).save()
#   OR give some specific filenames
#   app.UploadHandlerClass(request, ['image']).save()

class BaseUploadHandler(object):

    def __init__(self, request, require_names=None):
        self.request = request
        self.get_files(require_names)

    def get_files(self, require_names):
        if require_names:
            self.uploaded_fnames = [f for f in require_names if self.request.files.has_key(f)]
        else:
            self.uploaded_fnames = self.request.files.keys()

    def check(self):
        '''
        check the size of a file
        '''
        pass

    def save(self):
        pass

    def handle(self):
        self.check()
        self.save()


class LocalUploadHandler(BaseUploadHandler):
    FILE_DIR = '/tmp/upload/'

    @classmethod
    def _get_fullpath(cls, fname):
        return path.join(cls.FILE_DIR, fname)

    def _get_hashname(self, fname):
        filename = self.request.files.get(fname).filename
        f_list = filename.split('.')
        f_suffix = f_list[-1]
        seed = '{user_id}{fname}{time}'.format(user_id='', fname=filename, time=str(time()))
        return '{0}.{1}'.format(sha1(seed).hexdigest()[:16], f_suffix)

    def _save_handler(self, fname):
        hash_name = self._get_hashname(fname)
        full_path = self._get_fullpath(hash_name)
        f = self.request.files.get(fname)

        try:
            f.save(full_path)
            return {'path': full_path, 'filename': fname}
        except:
            return {'path': '', 'filename': fname}

    def save(self):
        return [self._save_handler(f) for f in self.uploaded_fnames]


UploadHanderFactory = GeneralFactory.gen()
UploadHanderFactory.backend_dict = {'local': LocalUploadHandler}
