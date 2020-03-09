

import os
import inspect
import datetime
import sys
from os import path
__level_list = ['CODE ', 'DEBUG', 'INFO ', 'WARN ', 'ERROR']
__initialized = False
__logger = None
__level_valve = 0
__filepath = ""


def init(file_path: str):
    global __logger, __initialized, __filepath
    if __logger is not None:
        print('Logger is already initialized.')
    else:
        if file_path:
            try:
                __logger = open(file_path, 'w')
                __filepath = file_path
            except IOError:
                print(
                    f'Logger is failed to open file {file_path}, the initialization is not valid.')
        else:
            __logger = sys.stdout
    __initialized = True


def is_init():
    return __initialized


def __log(info: str):
    print(info, file=__logger)
    if __logger:
        if __logger != sys.stdout:
            print(info)
        __logger.flush()


def set_level(level: int):
    global __level_valve
    __level_valve = level


def get_level():
    return __level_valve


def get_file():
    return __filepath


def log(level: int = 2, info: str = None):
    if not __initialized:
        raise RuntimeWarning(
            "A logging function was called when the logger is not initialized!")

    if level < __level_valve:
        return
    time_now = datetime.datetime.now().strftime("%H:%M:%S")

    previous_frame = inspect.currentframe().f_back
    (mf_name, line_number, caller_name, *_) = inspect.getframeinfo(previous_frame)

    module_name = mf_name
    if module_name != '<stdin>':
        module_name = path.splitext(path.basename(module_name))[0]

    caller = None
    if __level_valve > 0:
        caller = module_name
    else:
        caller = f'({module_name} -> {caller_name}@{line_number})'

    determined_level = __level_list[level] if \
        0 <= level <= len(__level_list)-1 \
        else 'UNKNOWN'
    __log(f'[{time_now} {determined_level}] {caller} : {info}')


def finalize():
    global __logger, __initialized
    if __logger:
        __logger.close()
    __logger = None
    __initialized = False
