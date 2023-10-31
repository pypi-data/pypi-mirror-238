#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# import lib here
import os
import sys
import time
from datetime import datetime


def findcaller(func):
    def wrapper(*args, **kwargs):
        # 获取调用该函数的文件名、函数名及行号
        filename =  sys._getframe(1).f_code.co_filename
        funcname =  sys._getframe(1).f_code.co_name 
        lineno = sys._getframe(1).f_lineno

        # 将原本的入参转变为列表，再把调用者的信息添加到入参列表中
        # args = list(args)
        # args.append(f'{os.path.basename(filename)}.{funcname}.{lineno}')
        kwargs = dict(kwargs)
        kwargs['filename'] = os.path.basename(filename)
        # kwargs['funcname'] = funcname
        kwargs['lineno'] = lineno
        func(*args, **kwargs)
    return wrapper

# Copy from https://github.com/ultralytics/yolov5/blob/4d687c8c56e3ee4e6851e48c1c5089c731ef0fcd/utils/general.py#L668:L691
def colorstr(*input):
    # Colors a string https://en.wikipedia.org/wiki/ANSI_escape_code, i.e.  colorstr('blue', 'hello world')
    *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])  # color arguments, string
    colors = {
        'black': '\033[30m',  # basic colors
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',  # bright colors
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'end': '\033[0m',  # misc
        'bold': '\033[1m',
        'underline': '\033[4m'}
    return ''.join(colors[x] for x in args) + f'{string}' + colors['end']

class SimLog(object):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
    _level = (INFO, WARNING, ERROR, CRITICAL)
    _colors = ('blue', 'yellow', 'red', 'bright_red')
    level_colors = {k: v for k, v in zip(_level, _colors)}
    def __init__(self, fpath='logs/log.txt') -> None:
        """简单的日志系统

        Args:
            fpath (str, optional): 日志文件保存的路径. Defaults to 'log.txt'.
        """
        log_dir = os.path.dirname(fpath)
        os.makedirs(log_dir, exist_ok=True)
        self.fpath = fpath
        print(f'Logging to the file: {fpath}')

    def get_time(self):
        """获取时间，精确到毫秒

        Returns:
            str: 时间
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]

    def log(self, msg=None, level='', console=True, end='', filename='', lineno=''):
        """打印日志信息

        Args:
            msg (str, optional): 要打印的信息. Defaults to None.
            level (str, optional): 日志等级. Defaults to ''.
            console (bool, optional): 保存到文件的同时打印到控制台. Defaults to True.
            end (str, optional): 行尾. Defaults to ''.
        """
        if not filename:
            filename =  os.path.basename(sys._getframe(1).f_code.co_filename)
        if not lineno:
            lineno = sys._getframe(1).f_lineno
        _msg = f'{self.get_time()} [{filename}:{lineno}] {(level+":" if level else ""):10}{msg}'
        with open(self.fpath, 'a', encoding='utf-8') as f:
            print(_msg, end=end, file=f)
        if console:
            if level in self._level:
                _msg = colorstr(self.level_colors.get(level), _msg)
            print(_msg, end=end)

    @findcaller
    def info(self, msg=None, console=True, end='', **kwargs):
        """打印普通信息

        Args:
            msg (str, optional): 要打印的信息. Defaults to None.
            console (bool, optional): 保存到文件的同时打印到控制台. Defaults to True.
            end (str, optional): 行尾. Defaults to ''.
        """
        self.log(msg, SimLog.INFO, console, end, **kwargs)

    @findcaller
    def warning(self, msg=None, console=True, end='', **kwargs):
        """打印警告信息

        Args:
            msg (str, optional): 要打印的信息. Defaults to None.
            console (bool, optional): 保存到文件的同时打印到控制台. Defaults to True.
            end (str, optional): 行尾. Defaults to ''.
        """
        self.log(msg, SimLog.WARNING, console, end, **kwargs)

    @findcaller
    def error(self, msg=None, console=True, end='', **kwargs):
        """打印错误信息

        Args:
            msg (str, optional): 要打印的信息. Defaults to None.
            console (bool, optional): 保存到文件的同时打印到控制台. Defaults to True.
            end (str, optional): 行尾. Defaults to ''.
        """
        self.log(msg, SimLog.ERROR, console, end, **kwargs)

    @findcaller
    def critical(self, msg=None, console=True, end='', **kwargs):
        """打印严重信息

        Args:
            msg (str, optional): 要打印的信息. Defaults to None.
            console (bool, optional): 保存到文件的同时打印到控制台. Defaults to True.
            end (str, optional): 行尾. Defaults to ''.
        """
        self.log(msg, SimLog.CRITICAL, console, end, **kwargs)


if __name__ == '__main__':
    sLog = SimLog('./logs/log_file.txt')
    sLog.log('这是第1条日志', end='\n')
    sLog.log('这是第2条日志', console=False, end='\n')

    sLog.info('这是第3条日志', end='\n')
    sLog.info('这是第4条日志', console=False, end='\n')
    time.sleep(3)
    sLog.log(end='\n')
    sLog.warning(end='\n')
    sLog.info([[1,2,3], [2,3,4]], end='\n')
    sLog.info({1:[1,2,3], 2:[2,3,4]}, end='\n')
    sLog.error('error msg', end='\n')
    sLog.critical('critical msg', end='\n')
    time.sleep(3)