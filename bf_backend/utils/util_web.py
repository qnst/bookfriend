# coding:utf-8
import datetime
import functools
import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse_lazy
from django.http import HttpResponsePermanentRedirect
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, TemplateView, DetailView

__author__ = 'sanyang'


def check_code(code):
    return 200 <= code <= 209


def check_permisions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # args 是肯定会有的，但 kwargs 不一定
        view = args[0]
        if isinstance(view, View):  # 兼容视图类和方法
            req = view.request
        else:
            req = args[0]
        current_path = req.META["PATH_INFO"]
        match = resolve(current_path, settings.ROOT_URLCONF)

        perm = match.url_name
        perms = req.session.get('perms')
        if not perms or perm not in perms:
            return HttpResponsePermanentRedirect(reverse_lazy("customer:no_auth"))

        # if not req.session.get('user', None):
        #     logging.info('#######  user is not in session, portal will logout  #####')
        #     return HttpResponsePermanentRedirect(reverse_lazy("customer:logout"))

        kwargs['customer_id'] = req.user.id
        kwargs['datacenter_id'] = req.session['datacenter']['default']['key']
        kwargs['project_id'] = req.session['project']['default']['id']
        return func(*args, **kwargs)
    return wrapper


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class ViewBase(View):
    @method_decorator(login_required)
    # @check_permisions
    def dispatch(self, request, *args, **kwargs):
        return super(ViewBase, self).dispatch(request, *args, **kwargs)

    @property
    def domain(self):
        return 'http://' + self.request.get_host()

    @property
    def input(self):
        """获取request传递过的所有参数"""
        i = {}
        # args = self.request.REQUEST
        args = self.request.GET or self.request.POST
        for item in args:
            i[item] = args[item]
        return i

    def get_argument(self, arg_name, default=''):
        if arg_name in self.input:
            return self.input[arg_name]
        else:
            return default

    def get_int(self, arg_name, default=0):
        if arg_name in self.input:
            return int(self.input[arg_name])
        else:
            return default


class ListViewBase(ListView, ViewBase):
    page = 1
    per_page = 10
    params = {}
    context_object_name = 'o_list'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page')

    def get_context_data(self, **kwargs):
        context = super(ListViewBase, self).get_context_data(**kwargs)
        context['request'] = self.request
        self.params = self.input.copy()
        self.params['page'] = self.request.GET.get('page')
        self.params['per_page'] = self.request.GET.get('per_page')
        context = dict(context, **self.params)
        return context


class DetailViewBase(DetailView, ViewBase):
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        logging.info(kwargs)
        context = super(DetailViewBase, self).get_context_data(**kwargs)
        context['request'] = self.request
        context = dict(context, **self.input)  # 把获取的参数附加到context中返回到前台
        return context


class TemplateViewBase(TemplateView, ViewBase):
    page = 1
    per_page = 10
    params = {}

    def get_context_data(self, **kwargs):
        context = super(TemplateViewBase, self).get_context_data(**kwargs)
        context['request'] = self.request
        self.params = self.input.copy()
        # self.params['page'] = self.request.GET.get('page', self.page)
        # self.params['per_page'] = self.request.GET.get('per_page', self.per_page)
        context.update(self.params)
        return context
