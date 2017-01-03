# coding=utf-8
import logging
import datetime
import uuid

from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.template import RequestContext

from django.contrib.auth.models import User
from models import MyProfile
from forms import UserForm, RegisterForm, ChangepwdForm

__author__ = 'sanyang'


def login_validate(request, username, password):
    res = False
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return True
    return res


def login(request):
    error = []
    if request.method == 'POST':
        next = request.POST.get("next", '/')
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            res = login_validate(request, username, password)
            if res:
                return HttpResponseRedirect(next)
            else:
                error.append('用户名或密码不正确')
    else:
        next = request.GET.get('next', '/')
        form = UserForm()
    return render_to_response('customer/login.html', {'form': form, 'error': error, 'next': next},
                              context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    next = reverse('customer:login')
    return HttpResponseRedirect(next)


def is_exists(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        value = request.POST.get('value')
        if 'username' == name:
            user = User.objects.filter(username=value)
        elif 'email' == name:
            user = User.objects.filter(email=value)
        else:
            user = None
        res = 'true' if user else 'false'
        return HttpResponse(res)


def register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password1 = data['password1']

            if not User.objects.all().filter(username=username):
                if form.pwd_validate(password, password1):
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    login_validate(request, username, password)
                    return HttpResponseRedirect('/')  # 注册完成后直接跳转到主页
                else:
                    error.append('请输入相同的密码')
            else:
                error.append('用户名已存在，请重新输入一个用户名')
    else:
        form = RegisterForm()
    return render_to_response('customer/login.html', {'form': form, 'error': error})


def forgot_pwd(request):  # todo 根据用户id，发送一份邮件
    if request.method == 'POST':
        email = request.POST.get('email')
        return JsonResponse({'code': 0, 'message': email})


def changepassword(request, username):
    error = []
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=username, password=data['old_pwd'])
            if user is not None:
                if data['new_pwd'] == data['new_pwd1']:
                    newuser = User.objects.get(username__exact=username)
                    newuser.set_password(data['new_pwd'])
                    newuser.save()
                    return HttpResponseRedirect('/login/')
                else:
                    error.append('请输入相同的密码')
            else:
                error.append('原始密码输入不正确')
    else:
        form = ChangepwdForm()
    return render_to_response('customer/changepassword.html', {'form': form, 'error': error})
