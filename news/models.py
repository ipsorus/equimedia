from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from equi_media_portal.singleton import SingletonModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NewsPost(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок новости")
    content = CKEditor5Field(blank=True, verbose_name="Содержание новости")
    image = models.ImageField(upload_to='media/news/%Y/%m/%d', blank=True, verbose_name="Постер для новости")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name="Публикация новости")
    source = models.CharField(max_length=150, blank=True, verbose_name="Источник новости")
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_news_posts',
                               default=1)

    def get_absolute_url(self):
        return reverse('news_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('news_post_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('news_post_delete', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Дата создания: {self.time_create} - {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class NewsSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название раздела на главной странице'), max_length=128, default='Актуальная новость')
    other_news_title = models.CharField(verbose_name=_('Название раздела под главной новостью'), max_length=128, default='Новости')
    title_news_page = models.CharField(verbose_name=_('Название в разделе "Новости"'), max_length=128, blank=True, default='Новости')
    sub_title_news_page = models.CharField(verbose_name=_('Текст под названием в разделе "Новости"'), max_length=128,
                                           blank=True, default='Узнавайте новости первыми')
    sticky_sidebar_news = models.BooleanField(verbose_name=_('Подвижный сайдбар в новостях'), default=True)
    subscribe_main_sidebar = models.BooleanField(verbose_name=_('Подписка в сайдбаре в новостях'), default=True)
    news_on_page = models.IntegerField(verbose_name=_('Количество видимых новостей без скроллинга'), default=6)
    sidebar_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32, default='Рекомендовано')

    def __str__(self):
        return 'Основные настройки блока "Новости"'

    class Meta:
        verbose_name = "Настройки раздела"
        verbose_name_plural = "Настройки раздела"


class BannerNewsSideBar1(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер в сайдбаре #1 (ширина 300px)'
        verbose_name_plural = 'Баннер в сайдбаре #1 (ширина 300px)'


class BannerNewsSideBar2(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер в сайдбаре #2 (ширина 300px)'
        verbose_name_plural = 'Баннер в сайдбаре #2 (ширина 300px)'


class BannerNewsBetweenNews(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.jpg', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер между новостями (ширина 720px)'
        verbose_name_plural = 'Баннер между новостями (ширина 720px)'
