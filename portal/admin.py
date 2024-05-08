from django.contrib import admin

from portal.models import News


class NewsAdmin(admin.ModelAdmin):
    model = News

admin.site.register(News, NewsAdmin)

