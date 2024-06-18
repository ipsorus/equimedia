from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
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


class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=255, verbose_name='Ваш электронный адрес (email)')
    content = models.TextField(verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя',  blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'Вам письмо от {self.email}'
