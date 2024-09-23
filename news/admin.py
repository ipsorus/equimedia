from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import ProgrammingError
from mptt.admin import DraggableMPTTAdmin

from news.models import NewsPost, NewsSettings, BannerNewsBetweenNews, BannerNewsSideBar1, BannerNewsSideBar2, Comment, \
    Rating, ViewCount
from slider.models import Slider


@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'post', 'author', 'time_create', 'status')
    mptt_level_indent = 2
    list_display_links = ('post',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)


class NewsAdmin(admin.ModelAdmin):
    model = NewsPost

    def delete_model(self, request, obj):
        try:
            slide = Slider.objects.get(news_id=obj.id)
        except ObjectDoesNotExist:
            slide = False

        obj.delete()

        if slide:
            slide.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            try:
                slide = Slider.objects.get(news_id=obj.id)
            except ObjectDoesNotExist:
                slide = False

            obj.delete()

            if slide:
                slide.delete()

    def save_model(self, request, obj, form, change):

        if change:
            o = self.model.objects.get(pk=obj.id)
            try:
                slide = Slider.objects.get(news_id=obj.id)
            except ObjectDoesNotExist:
                slide = False

            if obj.slider:
                if o.slider and slide:
                    super().save_model(request, obj, form, change)
                    slide.title = obj.title

                    file = ContentFile(obj.image.read())
                    file.name = obj.image.name.split('/')[-1]
                    slide.poster = file

                    slide.save()
                else:
                    super().save_model(request, obj, form, change)
                    try:
                        file = ContentFile(obj.image.read())
                        file.name = obj.image.name.split('/')[-1]
                        slide = Slider.objects.create(title=obj.title,
                                                      poster=file,
                                                      is_published=True,
                                                      url=obj.get_absolute_url(),
                                                      news_id=obj.id)
                        slide.save()
                    except:
                        pass
            else:
                super().save_model(request, obj, form, change)
                if slide:
                    try:
                        slide.delete()
                    except:
                        pass
        else:
            super().save_model(request, obj, form, change)
            if obj.slider:
                try:
                    file = ContentFile(obj.image.read())
                    file.name = obj.image.name.split('/')[-1]
                    slide = Slider.objects.create(title=obj.title,
                                                  poster=file,
                                                  is_published=True,
                                                  url=obj.get_absolute_url(),
                                                  news_id=obj.id)
                    slide.save()
                except:
                    pass


class NewsSettingsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            NewsSettings.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


class BannerNewsSideBar1Admin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            BannerNewsSideBar1.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


class BannerNewsSideBar2Admin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            BannerNewsSideBar2.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


class BannerNewsBetweenNewsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            BannerNewsBetweenNews.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


class RatingsAdmin(admin.ModelAdmin):
    model = Rating


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rating, RatingsAdmin)

admin.site.register(NewsPost, NewsAdmin)
admin.site.register(NewsSettings, NewsSettingsAdmin)
admin.site.register(BannerNewsSideBar1, BannerNewsSideBar1Admin)
admin.site.register(BannerNewsSideBar2, BannerNewsSideBar2Admin)
admin.site.register(BannerNewsBetweenNews, BannerNewsBetweenNewsAdmin)