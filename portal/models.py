from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from equi_media_portal.singleton import SingletonModel


class SocialsSettings(SingletonModel):
    social_whatsapp_url = models.URLField(verbose_name=_('Ссылка на Whatsapp'), max_length=256, blank=True, default='https://api.whatsapp.com/')
    social_telegram_url = models.URLField(verbose_name=_('Ссылка на Telegram'), max_length=256, blank=True, default='https://t.me/')
    social_youtube_url = models.URLField(verbose_name=_('Ссылка на Youtube'), max_length=256, blank=True, default='https://www.youtube.com/')
    social_vk_url = models.URLField(verbose_name=_('Ссылка на VK'), max_length=256, blank=True, default='https://vk.com/')
    social_instagram_url = models.URLField(verbose_name=_('Ссылка на Instagram'), max_length=256, blank=True, default='https://instagram.com/')
    social_twitter_url = models.URLField(verbose_name=_('Ссылка на Twitter'), max_length=256, blank=True, default='https://twitter.com/')
    social_pinterest_url = models.URLField(verbose_name=_('Ссылка на Pinterest'), max_length=256, blank=True, default='https://ru.pinterest.com/')

    def __str__(self):
        return 'Настройки социальных сетей'

    class Meta:
        verbose_name = "Социальные сети"
        verbose_name_plural = "Социальные сети"


class SiteSettings(SingletonModel):
    site_url = models.URLField(verbose_name=_('Адрес сайта'), max_length=128, blank=True, default='http://www.example.ru')
    title = models.CharField(verbose_name=_('Название сайта'), max_length=128, default='КСК Виват-Россия!')
    alter_title = models.CharField(verbose_name=_('Второе название для сайта'), max_length=128, blank=True)
    favicon = models.ImageField(upload_to='media/favicon/%Y/%m/%d', default='images/favicon/favicon.ico', verbose_name='Иконка сайта', blank=True)
    phone = models.CharField(verbose_name=_('Телефон в футере'), max_length=32, default='8 (495) 632-52-11')
    email = models.CharField(verbose_name=_('E-mail в футере'), max_length=128, default='info@equimedia.ru')
    current_year = models.CharField(verbose_name=_('Текущий год в футере'), max_length=4, default='2024')
    keywords_seo = models.TextField(verbose_name=_('Ключевые слова для SEO'), max_length=256, blank=True)
    description_seo = models.TextField(verbose_name=_('Описание сайта для SEO'), max_length=256, blank=True)

    def __str__(self):
        return 'Основные настройки сайта'

    class Meta:
        verbose_name = "Основные настройки сайта"
        verbose_name_plural = "Основные настройки сайта"


class AboutUsSettings(SingletonModel):
    title_about_us = models.CharField(verbose_name=_('Текст в заголовке "О нас" на главной странице'), max_length=50, default='Узнайте больше о нас')
    big_title_about_us = models.CharField(verbose_name=_('Жирный текст в заголовке "О нас" на главной странице'),
                                          max_length=30, default='Все ресурсы – в одном месте')
    about_us_text = models.TextField(verbose_name=_('Текст в разделе "О нас" на главной странице'), max_length=1024, default='На нашей площадке вы можете пройти онлайн-курсы по посадке, выездке, конкуру, ветеринарии, кормлению,  конному английскому или немецкому, повысить квалификацию как тренера или в сфере коневодства')
    poster_about_us = models.ImageField(upload_to='media/about_us/poster/%Y/%m/%d', default='images/about_us/1000.jpg',
                                        verbose_name='Обложка для раздела "О нас"')

    def __str__(self):
        return 'Настройка страницы "О нас" на главной странице'

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class ContactsSettings(SingletonModel):
    phone1 = models.CharField(verbose_name=_('Телефон 1'), max_length=32, default='8 (495) 632-52-11')
    phone2 = models.CharField(verbose_name=_('Телефон 2'), max_length=32, blank=True, default='8 (495) 111-22-33')
    email = models.CharField(verbose_name=_('E-mail'), max_length=128, default='info@equimedia.ru')
    address = models.CharField(verbose_name=_('Адрес'), max_length=128, default='Московская область, Ленинский городской округ, сельское поселение Молоковское.')
    poster_contacts = models.ImageField(upload_to='media/contacts/poster/%Y/%m/%d', default='images/contacts/contacts.webp',
                                        verbose_name='Обложка для раздела "Контакты"')

    def __str__(self):
        return 'Настройка страницы "Контакты"'

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"


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
