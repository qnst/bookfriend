# coding: utf-8
import functools
import logging
import threading
import time

__author__ = 'wangsy'


# 表示如果spider的 pipeline 属性中包含了添加该注解的pipeline，则执行该pipeline，否则跳过该pipeline
def check_spider_pipeline(process_item_method):
    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)
        # 如果spider的 pipeline 属性中包含了添加该注解的pipeline，则执行该pipelin
        if self.__class__ in spider.pipeline:
            return process_item_method(self, item, spider)
        else:  # 否则跳过该pipeline
            logging.info(msg % 'skipping')
            return item

    return wrapper


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


# 记住每个函数的计算结果
def memo(func):
    cache = {}

    @functools.wraps(func)
    def wrap(*arg):
        if arg not in cache:
            cache[arg] = func(*arg)
        return cache[arg]

    return wrap


# 有錯誤信息繼續執行，并把錯誤信息記錄下來
def check_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            logging.error(e)  # todo 應該把這裡的錯誤信息記錄下來

    return wrapper
