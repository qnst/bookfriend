# coding: utf-8

import django_filters
from rest_framework import viewsets, filters

from book.models import Category, Book
from serializers import CategorySerializer, BookSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_fields = ('author', 'status')