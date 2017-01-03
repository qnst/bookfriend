#coding:utf-8
from django.conf.urls import url,patterns
from django.views.generic import TemplateView
from views import *

urlpatterns=patterns(
    "",
    url(r"^login/", login, name="login"),
    url(r"^logout/", logout, name="logout"),
    url(r"^forgot_pwd/", forgot_pwd, name="forgot_pwd"),
    url(r"^is_exists/", is_exists, name="is_exists"),
    url(r"^register/", register, name="register"),
)

