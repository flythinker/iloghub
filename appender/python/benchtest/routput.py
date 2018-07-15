#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lyon Walker
# @Email   : 18192409520@163.com
# @File    : output.py
# @Time    : 18/07/15 9:42

from rqueue import RedisQueue
import time

def routput():
    q = RedisQueue('test', host='139.196.79.196', password='0okmnhy6', port=6379, db=0)
    while 1:
        result = q.get_nowait()
        if not result:
            break
        print("output.py: data {} out of queue {}".format(result, time.strftime("%c")))
        time.sleep(0.01)


