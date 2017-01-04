# coding: utf-8
from __future__ import unicode_literals, absolute_import

import django_filters
from rest_framework import permissions, viewsets, filters, renderers
from rest_framework.response import Response
from rest_framework.decorators import (
    permission_classes, detail_route
)

from .serializers import CategorySerializer, BookSerializer
from book.models import Category, Book

# 参考：　https://blog.laisky.com/p/django-rest/

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    permission_classes = (permissions.IsAuthenticated,)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_fields = ('title', 'ISBN')

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('title', 'ISBN', 'created_at')  # http://example.com/api/users?ordering=title,-created_at

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')  # http://example.com/api/users?search=title

    # def filter_queryset(self, request, queryset, view):
    #     nodename = request.QUERY_PARAMS.get('title')
    #     if nodename:
    #         return queryset.filter(nodename=nodename)
    #     else:
    #         return queryset

    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    # def plaintext(self, request, *args, **kwargs):
    #     """自定义 Api 方法"""
    #     model = self.get_object()
    #     return Response(repr(model))