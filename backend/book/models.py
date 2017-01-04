# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


# 参考: http://www.tuicool.com/articles/z2uyyiY

class BaseModel(models.Model):
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True
        # ordering = ['created_at']

    def __unicode__(self):
        return getattr(self, 'name', '') or getattr(self, 'title', '')


class Category(BaseModel):
    name = models.CharField('名称', max_length=32)
    description = models.TextField('描述', null=True, blank=True)

    class Meta:
        db_table = 'b_category'
        verbose_name_plural = verbose_name = '图书类别'


class Tag(BaseModel):
    name = models.CharField('名称', max_length=32)
    description = models.TextField('描述', null=True, blank=True)

    class Meta:
        db_table = 'b_tag'
        verbose_name_plural = verbose_name = '图书标签'


class Author(BaseModel):
    name = models.CharField('姓名', max_length=128)
    description = models.TextField('描述', null=True, blank=True)

    class Meta:
        db_table = 'b_author'
        verbose_name_plural = verbose_name = '作者'


class Publisher(BaseModel):
    name = models.CharField('名称', max_length=128)
    description = models.TextField('描述', null=True, blank=True)
    address = models.CharField('地址', max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'b_publisher'
        verbose_name_plural = verbose_name = '出版社'


class Book(BaseModel):
    STATUS_SET = (
        (0, "隐藏"),
        (1, "显示"),
    )
    title = models.CharField('标题', max_length=128)
    ISBN = models.CharField('ISBN', max_length=50, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, related_name='p_books', verbose_name='出版社', null=True, blank=True)
    publish_date = models.DateField('出版年', null=True, blank=True)
    page_num = models.IntegerField('页数', null=True, blank=True)
    money = models.FloatField('定价', null=True,  blank=True)
    description = models.TextField('描述', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='c_books', verbose_name='类别', null=True, blank=True)
    douban_score = models.FloatField('豆瓣评分', null=True, blank=True)
    douban_score_num = models.IntegerField('豆瓣评分人数', null=True, blank=True)
    status = models.IntegerField(choices=STATUS_SET, default=0, verbose_name='状态')

    authors = models.ManyToManyField(Author, related_name='a_books', verbose_name='作者')
    tags = models.ManyToManyField(Tag, related_name='t_books', verbose_name='标签')
    users = models.ManyToManyField(User, related_name='u_books', verbose_name='拥有者')

    class Meta:
        db_table = 'book'
        verbose_name_plural = verbose_name = '图书'


class Score(BaseModel):
    DEGREE_SET = (
        (1, '一星'),
        (2, '二星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星'),
    )
    degree = models.IntegerField(choices=DEGREE_SET, default=3, verbose_name='评分')
    user = models.ForeignKey(User, related_name='u_scores', verbose_name='评分人')
    book = models.ForeignKey(Book, related_name='b_scores', verbose_name='书本')

    class Meta:
        db_table = 'b_score'
        verbose_name_plural = verbose_name = '评分'

    def __unicode__(self):
        return self.degree


class Comment(BaseModel):
    content = models.TextField('内容')
    creator = models.ForeignKey(User, related_name='u_comments', verbose_name='评论者')
    book = models.ForeignKey(Book, related_name='b_comments', verbose_name='书本')

    class Meta:
        db_table = 'b_comment'
        verbose_name_plural = verbose_name = '评论'

    def __unicode__(self):
        return self.degree[0, 20]


class Checkout(BaseModel):
    CHECKOUT_SET = (
        (0, '借书中'),
        (1, '阅读中'),
        (2, '已返还'),
    )
    book = models.ForeignKey(Book, related_name='b_checkouts', verbose_name='书本')
    borrow_in = models.ForeignKey(User, related_name='u_checkout_ins', verbose_name='借入者')
    borrow_out = models.ForeignKey(User, related_name='u_checkout_outs', verbose_name='借出者')
    status = models.IntegerField(choices=CHECKOUT_SET, default=0, verbose_name='状态')

    class Meta:
        db_table = 'b_checkout'
        verbose_name_plural = verbose_name = '借书记录'

    def __unicode__(self):
        return self.book



