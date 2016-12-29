# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from restfulapi.urls import router

from django.contrib import admin
admin.autodiscover()

# import xadmin
# xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
# from xadmin.plugins import xversion
# xversion.register_models()

urlpatterns = patterns(
    '',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^setlang/$', 'django.views.i18n.set_language', name='setlang'),  # 全局语言设置
    url(r'^admin/', include(admin.site.urls)),  # 后台管理模块

    # restfulapi
    url(r'^api/', include(router.urls, namespace="api")),
    url(r'^book/', include(book.urls, namespace="book")),
    url(r'^customer/', include(router.urls, namespace="customer")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)