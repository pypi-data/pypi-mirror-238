# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : goalkeeper.py
@Date    : 2023/11/2 16:47:18
@Author  : zhchen
@Desc    : 守门员
"""
import time

SCOREBOARD = {}


def shooting(ball_name, duration=60 * 10) -> bool:
    """在一定时间内的球被阻拦, 默认10分钟"""
    now = int(time.time())
    if ball_name not in SCOREBOARD:
        SCOREBOARD[ball_name] = now
        return True
    if now - SCOREBOARD[ball_name] > duration:
        SCOREBOARD[ball_name] = now
        return True
    return False
