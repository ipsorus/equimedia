from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from equi_media_portal.singleton import SingletonModel


class Category(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name="Название категории")

    def __str__(self):
        return f'{self.title}'


class WebsiteSettings(models.Model):
    language = models.CharField(max_length=16, unique=True, choices=settings.LANGUAGES, verbose_name=_('Language'))
    site_title = models.TextField(blank=True, verbose_name=_('Site title'))
    site_description = models.TextField(blank=True, verbose_name=_('Site description'))

    class Meta:
        verbose_name = _('website settings')
        verbose_name_plural = _('website settings')
        ordering = ['language']

    def __str__(self):
        # return dict(settings.LANGUAGES).get(self.language, self.language)
        return f'{self.language}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SiteSettings(SingletonModel):
    site_url = models.URLField(verbose_name=_('Website url'), max_length=256)
    title = models.CharField(verbose_name=_('Title'), max_length=256)

    def __str__(self):
        return 'Configuration'
