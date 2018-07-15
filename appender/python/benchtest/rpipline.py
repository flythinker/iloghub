#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lyon Walker
# @Email   : 18192409520@163.com
# @File    : rpipline.py
# @Time    : 18/07/15 9:33

# -*- coding:utf-8 -*-

import redis
import time
from concurrent.futures import ProcessPoolExecutor

r = redis.Redis(host='10.9.2.62', port=6379, password='0okmnhy6')


def try_pipeline():
    start = time.time()
    with r.pipeline(transaction=False) as p:
        p.sadd('seta', 1).sadd('seta', 2).srem('seta', 2).lpush('lista', 1).lrange('lista', 0, -1)
        p.execute()
    print(time.time() - start)


def without_pipeline():
    start = time.time()
    r.sadd('seta', 1)
    r.sadd('seta', 2)
    r.srem('seta', 2)
    r.lpush('lista', 1)
    r.lrange('lista', 0, -1)
    print(time.time() - start)


def worker():
    while True:
        try_pipeline()

with ProcessPoolExecutor(max_workers=20) as pool:
    for _ in range(10):
        pool.submit(worker)

