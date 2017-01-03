# coding=utf-8
from django import http
from django.views.debug import technical_500_response
from django.conf import settings
import sys

__author__ = 'sanyang'


class BlockedIpMiddleware(object):
    """IP黑名单"""
    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in getattr(settings, "BLOCKED_IPS", []):
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     pass
    #
    # def process_exception(self, request, exception):
    #     pass
    #
    # def process_response(self, request, response):
    #     pass


class UserBasedExceptionMiddleware(object):
    """正式环境，限制只有部分IP可以看到调试信息"""
    def process_exception(self, request, exception):
        # if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())


class UserDefinedResponse(object):
    pass


# 模板中可以直接访问这里字典中的值，如{{ test }}
def add_vars_to_response(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'test': 'test'}