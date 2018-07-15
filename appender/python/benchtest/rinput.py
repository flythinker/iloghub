#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lyon Walker
# @Email   : 18192409520@163.com
# @File    : input.py
# @Time    : 18/07/15 9:41

from rqueue import RedisQueue
import time
from random import Random


nums = 50 # 
pcs = 10 #

def random_str(randomlength=100):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789' * 20
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
        #print(len(str))
    return str


def rinput():
    c = 0
    q = RedisQueue('test', host='139.196.79.196', password='0okmnhy6', port=6379, db=0)  # 新建队列名为test
    for i in range(nums):
        random_str()
        q.put(str)
        print("input.py: data {} enqueue {}".format(str, time.strftime("%c")))
        time.sleep(1/pcs)
        c += 1
        print(c)
        if c > nums:
            break




