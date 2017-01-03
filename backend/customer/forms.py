# coding=utf-8
from models import MyProfile
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(label='Confirm', widget=forms.PasswordInput)

    def pwd_validate(self, p1, p2):
        return p1 == p2

class ChangepwdForm(forms.Form):
    old_pwd = forms.CharField()
    new_pwd = forms.CharField()
    new_pwd1 = forms.CharField()