# coding: utf-8
from __future__ import unicode_literals, absolute_import

import json

from rest_framework import serializers
from book.models import Category, Book


class MyCustField(serializers.CharField):
    """为 Model 中的自定义域额外写的自定义 Serializer Field"""

    def to_representation(self, obj):
        """将从 Model 取出的数据 parse 给 Api"""
        return obj

    def to_internal_value(self, data):
        """将客户端传来的 json 数据 parse 给 Model"""
        return json.loads(data.encode('utf-8'))


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'c_books')

        # 这句话的作用是为 MyModel 中的外键建立超链接，依赖于 urls 中的 name 参数
        # 不想要这个功能的话完全可以注释掉
        c_books = serializers.HyperlinkedRelatedField(
            many=True, queryset=Book.objects.all(),
            view_name='model-detail'
        )

class BookSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'cover', 'description', 'douban_score', 'users', 'tags')
        # read_only_fields = ('title',)


    def create(self, validated_data):
        """响应 POST 请求"""
        # 自动为用户提交的 model 添加 owner
        validated_data['owner'] = self.context['request'].user
        return Book.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """响应 PUT 请求"""
        instance.field = validated_data.get('field', instance.field)
        instance.save()
        return instance