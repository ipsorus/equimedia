from django.contrib import admin

from news.models import NewsPost


class NewsAdmin(admin.ModelAdmin):
    model = NewsPost


admin.site.register(NewsPost, NewsAdmin)
