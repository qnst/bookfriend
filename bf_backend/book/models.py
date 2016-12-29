# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('名称', max_length=32)


class Tag(models.Model):
    name = models.CharField('名称', max_length=32)


class Book(models.Model):
    STATUS_SET = (
        (0, "隐藏"),
        (1, "显示"),
    )
    title = models.CharField('标题', max_length=128)
    description = models.TextField('描述')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_SET, default=0)

    category = models.ForeignKey(Category, related_name='c_books')
    tags = models.ManyToManyField(Tag, related_name='t_books')
    users = models.ManyToManyField(User, related_name='u_books')

    class Meta:
        db_table = 'book'


class Score(models.Model):
    DEGREE_SET = (
        (1, '一星'),
        (2, '二星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星'),
    )
    degree = models.IntegerField(choices=DEGREE_SET)
    user = models.ForeignKey(User, related_name='u_scores')
    book = models.ForeignKey(Book, related_name='b_scores')


class Comment(models.Model):
    content = models.TextField('内容')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='u_comments')
    book = models.ForeignKey(Book, related_name='b_comments')


class Checkout(models.Model):
    CHECKOUT_SET = (
        (0, '未借阅'),
        (1, '阅读中'),
        (1, '已返还'),
    )
    book = models.ForeignKey(Book, related_name='b_checkouts')
    borrow_out = models.ForeignKey(User, related_name='u_checkout_outs')
    borrow_in = models.ForeignKey(User, related_name='u_checkout_ins')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=CHECKOUT_SET)




