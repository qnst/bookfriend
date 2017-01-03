# -*- coding: utf-8 -*-
import hashlib
import binascii
import json
import uuid
import datetime

__author__ = 'wangsy'


def sha1(basestring):
    hash = hashlib.sha1()
    hash.update(basestring)
    return hash.hexdigest()


def get_uuid():
    return binascii.b2a_hex(uuid.uuid4().bytes)


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


#convert object to a dict
def object2dict(obj):
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


#convert dict to object
def dict2object(d):
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
    else:
        inst = d
    return inst