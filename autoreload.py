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


_mtimes = {}
FILE_CHANGED = 3
def is_file_changed():
    for filename in gen_filenames():
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes.clear()
            return True
    return False


def check_file_changd():
    while True:
        if is_file_changed():
            sys.exit(FILE_CHANGED)
            time.sleep(1)


def wait_child(pid):
    while True:
        wpid, sts = os.waitpid(pid, 0)
        if os.WIFSTOPPED(sts):
            continue
            # if receive keybord interuption or kill signal
        elif os.WIFSIGNALED(sts):
            return -os.WTERMSIG(sts)
            # os.kill(os.getpid(), exit_code)
        elif os.WIFEXITED(sts):
            return os.WEXITSTATUS(sts)
        else:
            raise "Not stopped, signaled or exited???"


def handle_exit(exit_code):
    if exit_code < 0:
        os.kill(os.getpid(), exit_code)
    elif exit_code == FILE_CHANGED:
        pass
    else:
        sys.exit(exit_code)


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
            exit_code = wait_child(pid)
            handle_exit(exit_code)


def autoreload(func, *args, **kwargs):
    # child process
    if os.environ.get("RUN_MAIN") == "true":
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        check_file_changd()

    # parent process
    else:
        restart_reloader()
