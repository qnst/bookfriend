# coding=utf-8
from django.db import models


class Category(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=32)

    class Meta:
        db_table = 'category'


class Article(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    STATUS_SET = (
            (0, "草稿"),
            (1, "公开"),
    )
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_SET, default=0)
    category = models.ForeignKey(Category, related_name='entries')

    class Meta:
        db_table = 'article'