#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lyon Walker
# @Email   : 18192409520@163.com
# @File    : run.py
# @Time    : 18/07/15 9:49

from rinput import *
from routput import *
from concurrent.futures import ProcessPoolExecutor

def worker():
    while True:
        rinput()
        routput()

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=3) as pool:
        for _ in range(1):
            pool.submit(worker)
