# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : sche.py
@Date    : 2023/10/27 16:20:28
@Author  : zhchen
@Desc    : 
"""
import functools
from threading import Thread


def af(func):
    """异步跑函数"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


if __name__ == '__main__':
    import schedule


    @af
    def do_ship():
        print("123")


    schedule.every(2).seconds.do(do_ship)
    while True:
        schedule.run_pending()
