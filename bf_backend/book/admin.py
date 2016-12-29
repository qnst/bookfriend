from django.contrib import admin

from models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class ArticleAdmin(admin.ModelAdmin):
    pass