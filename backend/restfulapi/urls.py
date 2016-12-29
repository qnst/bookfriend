from django.conf.urls import patterns, url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'articles', views.ArticleViewSet)
