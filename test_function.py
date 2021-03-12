import numpy as np
import random
import sys
import os, psutil
import time

def decorator_duration(func):
    def wrapper():
        time_begin = time.time()
        func()
        print('Продолжительность работы: {}'.format(time.time()-time_begin))
    return wrapper

if __name__ == '__main__':
    @decorator_duration
    def test_func():
        history_ins = History()
        while True:
            score = random.random()
            ex = np.random.randint(low=1, high=10, size=500)
            if history_ins.set_history(ex, score) == False:
                print('Кол-во дублей: {}'.format(history_ins.count_dupl))
                break
    test_func()
