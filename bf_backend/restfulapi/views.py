# coding: utf-8

import django_filters
from rest_framework import viewsets, filters

from bf_backend.book.models import Category, Book
from serializers import CategorySerializer, ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = ArticleSerializer

    filter_fields = ('author', 'status')