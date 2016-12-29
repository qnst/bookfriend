# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
import datetime
#  参考 http://blog.csdn.net/svalbardksy/article/details/51199707


class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)


class Profile(object):
    __metaclass__ = ProfileBase


class MyProfile(Profile):
    SEX_SET = (
        (0, '女'),
        (1, '男'),
    )
    nickname = models.CharField(max_length=255, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    sex = models.IntegerField(choices=SEX_SET, default=0)
    location = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=30, blank=True)
    university = models.CharField(max_length=255, blank=True)
    # 可以在这里添加auth_user表的扩展字段

    def is_today_birthday(self):
        return self.birthday.date() == datetime.date.today()


# class Friend(models.Model):
#     user = models.ForeignKey(User, )
