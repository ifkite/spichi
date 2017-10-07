# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: autoreload.py
#          Desc: get some referance from django
#        Author: ifkite
#         Email: holahello@163.com
#      HomePage: http://github.com/ifkite
#      python version: 2.7.10
#    LastChange: 2017-07-30 22:27:38

# =============================================================================
'''

import sys
import os
import signal
import threading
import time


def clean_filenames(filenames):
    """
    """
    filelist = []
    for filename in filenames:
        # if not filename:
        #    continue
        # https://stackoverflow.com/questions/8822335/what-do-the-python-file-extensions-pyc-pyd-pyo-stand-for
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if os.path.exists(filename):
            filelist.append(filename)
    return filelist


def gen_filenames():
    modules = sys.modules.values()
    return clean_filenames([module.__file__ for module in modules if hasattr(module, '__file__')])


def walk_filenames():
    filelist = []
    start_dir = os.path.dirname(os.path.abspath(__file__))
    for dir_path, dirs, filenames in os.walk(start_dir):
        filelist.extend([
            os.path.join(dir_path, filename)
                for filename in filenames
                if filename.endswith('py') or filename.endswith('json')
                ])
    return filelist


_mtimes = {}
FILE_CHANGED = 3
def is_file_changed():
    for filename in walk_filenames():
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes.clear()
            return True
    return False


def check_file_changed():
    while True:
        time.sleep(1)
        if is_file_changed():
            os.kill(os.getpid(), signal.SIGKILL)


def wait_child(pid):
    while True:
        try:
            # wait for child process
            wpid, sts = os.waitpid(pid, 0)
        except KeyboardInterrupt:
            # handle exceptions when parent is waiting
            handle_parent_exit(pid)

        # if child process stopped
        if os.WIFSTOPPED(sts):
            continue
        # if receive keybord interuption or kill signal
        elif os.WIFSIGNALED(sts):
            return sts
        # seems not work
        elif os.WIFEXITED(sts):
            return sts
        else:
            raise "Not stopped, signaled or exited???"


def handle_child_exit(signal_code):
    # parent will fork a new child
    if signal_code == signal.SIGKILL:
        pass
    else:
        sys.exit()


def handle_parent_exit(pid):
    os.kill(pid, signal.SIGKILL)
    sys.exit()


def restart_reloader():
    while True:
        args = [sys.executable] + sys.argv
        child_environ = os.environ.copy()
        pid = os.fork()

        # child process
        if not pid:
            child_environ["RUN_MAIN"] = "true"
            # may exit with FILE_CHANGED code
            # in fact, call itself
            os.execve(sys.executable, args, child_environ)

        # parent process
        else:
            signal_code = wait_child(pid)
            handle_child_exit(signal_code)


# sample
# from wsgiref.simple_server import make_server
# def run():
#     httpd = make_server(host='', port=8848, app=app)
#     httpd.serve_forever()
# if __name__ == '__main__':
#     autoreload(run)

def autoreload(func, *args, **kwargs):
    # child process
    if os.environ.get("RUN_MAIN") == "true":
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        check_file_changed()

    # parent process
    else:
        restart_reloader()
