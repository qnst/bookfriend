# coding: utf-8
import functools
import hashlib
import logging
import threading
import time
import traceback
from django.conf import settings
from django.core.cache import cache
from util_django import *


__author__ = 'wangsy'


# 异步操作
def async(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


# 计算函数执行时间
def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)
        back = func(*args, **args2)
        print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__)
        return back

    return newFunc


def compute_key(function, args, kwargs):
    key = json.dumps((function.func_name, args, kwargs))
    return hashlib.sha1(key).hexdigest()


# 记住每个函数的计算结果
def memoize(duration=settings.SESSION_COOKIE_AGE):
    def _memoize(func):
        @functools.wraps(func)
        def __memoize(*args, **kwargs):
            key = compute_key(func, args, kwargs)

            # 如果存在于缓存中，直接返回（过期则取不到值）
            if key in cache:
                return cache.get(key)

            result = func(*args, **kwargs)
            cache.set(key, result, duration)
            return result

        return __memoize
    return _memoize


# 有錯誤信息繼續執行，并把錯誤信息記錄下來
def check_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            logging.error('========  %s  ========' % func.__name__)
            traceback.print_exc()

    return wrapper