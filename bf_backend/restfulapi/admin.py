from django.contrib import admin

from .models import Category, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('id',)
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ('id',)
    pass