# -*- coding: utf-8 -*-

import json
import datetime

from django import forms
from django.views.generic import ListView
from django.contrib.auth.decorators import  login_required
from django.core.urlresolvers import  RegexURLPattern
from django.http import HttpResponse
from django.db import models as md

__author__ = 'wangsy'


# 用于分页
class PageMix(object):
    def get_paginate_by(self, queryset):
        return self.request.GET.get("per_page")

    def get_context_data(self, **kwargs):
        context=ListView.get_context_data(self,**kwargs)
        context["per_page"]= self.request.GET.get("per_page")
        return context


# 对列表进行封装，然后返回
def json_res(objs):
        dst=[]
        for obj in objs:
            fields=[]  # 存储对象的属性名称
            for field in obj._meta.fields:
                fields.append(field.name)

            d = {}
            for attr in fields:
                if isinstance(getattr(obj, attr),datetime.datetime):
                    d[attr] = getattr(obj, attr).strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(getattr(obj, attr),datetime.date):
                    d[attr] = getattr(obj, attr).strftime('%Y-%m-%d')
                elif isinstance(getattr(obj, attr),md.Model):  # 如果属性值是django中内置model对象，或继承model的对象，只要id
                    d[attr] = getattr(obj, attr).id
                else:
                    d[attr] = getattr(obj, attr)
            dst.append(d)
        return HttpResponse(json.dumps(dst),content_type="application/json")


# 指定的url访问需要login_required
def lr_patt(urlpatterns,exp_name=[]):
    u=[]
    for _url in urlpatterns:
        if _url.name not in exp_name:
            s=RegexURLPattern(_url.regex.pattern,login_required(_url.callback),name=_url.name)
            u.append(s)
        else:
            u.append(_url)
    return u

# 获取IP
def get_client_ip(request):
    try:
        regip = request.META['HTTP_X_REAL_IP']
    except:
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
            regip = real_ip.split(",")[0]
        except:
            regip = request.META['REMOTE_ADDR']
    return regip

class BaseOSSForm(forms.Form):
    list_visible = ()

    list_hidden = ()

    def visible_fields(self):
        if self.list_visible:
            return [field for field in self if field.name in self.list_visible]
        return self

    def hidden_fields(self):
        if self.list_hidden:
            return [field for field in self if field.name in self.list_hidden]
        return []