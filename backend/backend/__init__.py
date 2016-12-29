#coding:utf-8

# 下面这句引用的意思：禁用 implicit relative import, 但并不会禁掉 explicit relative import.
# 例如， 推荐 from .celery import app， 不推荐 import celery.app
# 这样以后: 局部的包将不能覆盖全局的包, 本地的包必须使用相对引用了
from __future__ import absolute_import
