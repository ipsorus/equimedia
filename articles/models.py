from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from equi_media_portal.singleton import SingletonModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок статьи")
    content = CKEditor5Field(blank=True, verbose_name="Содержание статьи")
    image = models.ImageField(upload_to='media/articles/%Y/%m/%d', blank=True, verbose_name="Постер для статьи")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name="Публикация статьи")
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT,
                               related_name='author_article_posts',
                               default=1)

    def get_absolute_url(self):
        return reverse('article_detail_url', kwargs={'article_id': self.id})

    def get_update_url(self):
        return reverse('article_update_url', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('article_delete_url', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Дата создания: {self.time_create} - {self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class ArticlesSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название раздела на главной странице'), max_length=128, default='Статьи')
    other_articles_title = models.CharField(verbose_name=_('Название раздела под главной статьей'), max_length=128, default='Другие статьи')
    title_articles_page = models.CharField(verbose_name=_('Название в разделе "Статьи"'), max_length=128, blank=True, default='Статьи')
    sub_title_articles_page = models.CharField(verbose_name=_('Текст под названием в разделе "Статьи"'), max_length=128,
                                               blank=True, default='Лента интересных и полезных статей от нашей редакции')
    sticky_sidebar_articles = models.BooleanField(verbose_name=_('Подвижный сайдбар в статьях'), default=True)
    gallery_articles_sidebar = models.BooleanField(verbose_name=_('Галерея в сайдбаре в статьях'), default=True)
    articles_on_page = models.IntegerField(verbose_name=_('Количество видимых статей без скроллинга'), default=6)
    sidebar_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32, default='Рекомендуем')

    def __str__(self):
        return 'Основные настройки блока "Статьи"'

    class Meta:
        verbose_name = "Настройки раздела"
        verbose_name_plural = "Настройки раздела"


class BannerArticleSideBar1(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер в сайдбаре #1 (ширина 300px)'
        verbose_name_plural = 'Баннер в сайдбаре #1 (ширина 300px)'


class BannerArticleSideBar2(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер в сайдбаре #2 (ширина 300px)'
        verbose_name_plural = 'Баннер в сайдбаре #2 (ширина 300px)'


class BannerArticleBetweenArticles(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.jpg', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер между статьями (ширина 720px)'
        verbose_name_plural = 'Баннер между статьями (ширина 720px)'
