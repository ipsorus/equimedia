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


class SocialsSettings(SingletonModel):
    social_whatsapp_url = models.URLField(verbose_name=_('Ссылка на Whatsapp'), max_length=256, blank=True)
    social_telegram_url = models.URLField(verbose_name=_('Ссылка на Telegram'), max_length=256, blank=True)
    social_youtube_url = models.URLField(verbose_name=_('Ссылка на Youtube'), max_length=256, blank=True)
    social_vk_url = models.URLField(verbose_name=_('Ссылка на VK'), max_length=256, blank=True)
    social_instagram_url = models.URLField(verbose_name=_('Ссылка на Instagram'), max_length=256, blank=True)
    social_twitter_url = models.URLField(verbose_name=_('Ссылка на Twitter'), max_length=256, blank=True)
    social_pinterest_url = models.URLField(verbose_name=_('Ссылка на Pinterest'), max_length=256, blank=True)

    def __str__(self):
        return 'Настройки социальных сетей'


class NewsSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название раздела на главной странице'), max_length=128)
    other_news_title = models.CharField(verbose_name=_('Название раздела под главной новостью'), max_length=128)
    title_news_page = models.CharField(verbose_name=_('Название в разделе "Новости"'), max_length=128, blank=True)
    sub_title_news_page = models.CharField(verbose_name=_('Текст под названием в разделе "Новости"'), max_length=128,
                                           blank=True)
    sticky_sidebar_news = models.BooleanField(verbose_name=_('Подвижный сайдбар в новостях'), default=True)
    subscribe_main_sidebar = models.BooleanField(verbose_name=_('Подписка в сайдбаре в новостях'), default=True)
    news_on_page = models.IntegerField(verbose_name=_('Количество видимых новостей без скроллинга'), default=6)
    sidebar_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32)

    def __str__(self):
        return 'Основные настройки блока "Новости"'


class ArticlesSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название раздела на главной странице'), max_length=128)
    other_articles_title = models.CharField(verbose_name=_('Название раздела под главной статьей'), max_length=128)
    title_articles_page = models.CharField(verbose_name=_('Название в разделе "Статьи"'), max_length=128, blank=True)
    sub_title_articles_page = models.CharField(verbose_name=_('Текст под названием в разделе "Статьи"'), max_length=128,
                                               blank=True)
    sticky_sidebar_articles = models.BooleanField(verbose_name=_('Подвижный сайдбар в статьях'), default=True)
    gallery_articles_sidebar = models.BooleanField(verbose_name=_('Галерея в сайдбаре в статьях'), default=True)
    articles_on_page = models.IntegerField(verbose_name=_('Количество видимых статей без скроллинга'), default=6)
    sidebar_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32)

    def __str__(self):
        return 'Основные настройки блока "Статьи"'


class SliderSettings(SingletonModel):
    announcement_slider = models.BooleanField(verbose_name=_('Анонс новостей в слайдере'), default=True)
    pagination_dots = models.BooleanField(verbose_name=_('Пагинатор на слайдере'), default=True)
    scroller = models.BooleanField(verbose_name=_('Анимация скролла на слайдере'), default=True)

    def __str__(self):
        return 'Основные настройки блока "Слайдер"'


class BlogSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название блока на главной странице'), max_length=64)
    title_blog_page = models.CharField(verbose_name=_('Название в разделе "Блоги"'), max_length=128, blank=True)
    sub_title_blog_page = models.CharField(verbose_name=_('Текст под названием в разделе "Блоги"'), max_length=128,
                                           blank=True)
    last_comments = models.BooleanField(verbose_name=_('Последние комментарии в блогах'), default=True)
    recent_posts = models.BooleanField(verbose_name=_('Блок "Может быть интересно" в блогах'), default=True)
    sidebar_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32)
    posts_on_page = models.IntegerField(verbose_name=_('Количество видимых постов без скроллинга'), default=6)

    def __str__(self):
        return 'Основные настройки блока "Блоги"'


class SiteSettings(SingletonModel):
    site_url = models.URLField(verbose_name=_('Адрес сайта'), max_length=128, blank=True)
    title = models.CharField(verbose_name=_('Название сайта'), max_length=128)
    alter_title = models.CharField(verbose_name=_('Второе название для сайта'), max_length=128, blank=True)
    favicon = models.ImageField(upload_to='media/favicon/%Y/%m/%d', default='images/favicon/favicon.ico', verbose_name='Иконка сайта', blank=True)
    phone = models.CharField(verbose_name=_('Телефон в футере'), max_length=32)
    email = models.CharField(verbose_name=_('E-mail в футере'), max_length=128)
    current_year = models.CharField(verbose_name=_('Текущий год в футере'), max_length=4)
    keywords_seo = models.TextField(verbose_name=_('Ключевые слова для SEO'), max_length=256, blank=True)
    description_seo = models.TextField(verbose_name=_('Описание сайта для SEO'), max_length=256, blank=True)

    def __str__(self):
        return 'Основные настройки сайта'


class AboutUsSettings(SingletonModel):
    title_about_us = models.CharField(verbose_name=_('Текст в заголовке "О нас" на главной странице'), max_length=50)
    big_title_about_us = models.CharField(verbose_name=_('Жирный текст в заголовке "О нас" на главной странице'),
                                          max_length=30)
    about_us_text = models.TextField(verbose_name=_('Текст в разделе "О нас" на главной странице'), max_length=1024)
    poster_about_us = models.ImageField(upload_to='media/about_us/poster/%Y/%m/%d', default='images/about_us/1000.jpg',
                                        verbose_name='Обложка для раздела "О нас"')

    def __str__(self):
        return 'Настройка страницы "О нас" на главной странице'


class ContactsSettings(SingletonModel):
    phone1 = models.CharField(verbose_name=_('Телефон 1'), max_length=32)
    phone2 = models.CharField(verbose_name=_('Телефон 2'), max_length=32, blank=True)
    email = models.CharField(verbose_name=_('E-mail'), max_length=128)
    address = models.CharField(verbose_name=_('Адрес'), max_length=128)
    poster_contacts = models.ImageField(upload_to='media/contacts/poster/%Y/%m/%d', default='images/contacts/contacts.webp',
                                        verbose_name='Обложка для раздела "Контакты"')

    def __str__(self):
        return 'Настройка страницы "Контакты"'


class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=255, verbose_name='Ваш электронный адрес (email)')
    content = models.TextField(verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'Вам письмо от {self.email}'
