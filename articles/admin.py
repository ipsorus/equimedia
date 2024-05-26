from django.contrib import admin

from articles.models import Article


class ArticlesAdmin(admin.ModelAdmin):
    model = Article


admin.site.register(Article, ArticlesAdmin)
