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
        verbose_name = _("Социальные сети")
        verbose_name_plural = _("Социальные сети")


class SiteSettings(SingletonModel):
    site_maintenance = models.BooleanField(verbose_name=_('Отключить сайт на обслуживание'), default=False)
    site_url = models.URLField(verbose_name=_('Адрес сайта'), max_length=128, blank=True, default='http://www.example.ru')
    title = models.CharField(verbose_name=_('Название сайта'), max_length=128, default='КСК Виват-Россия!')
    alter_title = models.CharField(verbose_name=_('Второе название для сайта'), max_length=128, blank=True)
    favicon = models.ImageField(upload_to='media/favicon/%Y/%m/%d', default='images/favicon/favicon.ico', verbose_name=_('Иконка сайта'), blank=True)
    phone = models.CharField(verbose_name=_('Телефон в футере'), max_length=32, default='8 (495) 632-52-11')
    email = models.CharField(verbose_name=_('E-mail в футере'), max_length=128, default='info@equimedia.ru')
    current_year = models.CharField(verbose_name=_('Текущий год в футере'), max_length=4, default='2024')
    keywords_seo = models.TextField(verbose_name=_('Ключевые слова для SEO'), max_length=256, blank=True)
    description_seo = models.TextField(verbose_name=_('Описание сайта для SEO'), max_length=256, blank=True)
    gallery_url = models.URLField(verbose_name=_('Ссылка на галерею'), max_length=128, blank=True, default='http://www.gallery.ex')

    def __str__(self):
        return 'Основные настройки сайта'

    class Meta:
        verbose_name = _("Основные настройки сайта")
        verbose_name_plural = _("Основные настройки сайта")


class AboutUsSettings(SingletonModel):
    show_page = models.BooleanField(verbose_name=_('Отображать страницу'), default=True)
    show_testimonials = models.BooleanField(verbose_name=_('Отображать блок отзывов'), default=True)
    title_about_us = models.CharField(verbose_name=_('Название страницы'), max_length=50, default='О нас')
    big_title_about_us = models.CharField(verbose_name=_('Заголовок рядом с картинкой'),
                                          max_length=30, default='Все ресурсы – в одном месте')
    about_us_text = models.TextField(verbose_name=_('Текст описания'), max_length=1024, default='На нашей площадке вы можете пройти онлайн-курсы по посадке, выездке, конкуру, ветеринарии, кормлению,  конному английскому или немецкому, повысить квалификацию как тренера или в сфере коневодства')
    poster_about_us = models.ImageField(upload_to='media/about_us/poster/%Y/%m/%d', default='images/about_us/1000.jpg',
                                        verbose_name=_('Обложка для раздела "О нас"'))

    block1_title = models.CharField(verbose_name=_('Заголовок блока 1'), blank=True, max_length=50, default='Заголовок блока 1')
    block1_content = models.TextField(verbose_name=_('Текст блока 1'), blank=True, max_length=160, default='Текст блока 1. Краткое описание предлагаемых услуг')
    block2_title = models.CharField(verbose_name=_('Заголовок блока 2'), blank=True, max_length=50, default='Заголовок блока 2')
    block2_content = models.TextField(verbose_name=_('Текст блока 2'), blank=True, max_length=160, default='Текст блока 2. Краткое описание предлагаемых услуг')
    block3_title = models.CharField(verbose_name=_('Заголовок блока 3'), blank=True, max_length=50, default='Заголовок блока 3')
    block3_content = models.TextField(verbose_name=_('Текст блока 3'), blank=True, max_length=160, default='Текст блока 3. Краткое описание предлагаемых услуг')
    block4_title = models.CharField(verbose_name=_('Заголовок блока 4'), blank=True, max_length=50, default='Заголовок блока 4')
    block4_content = models.TextField(verbose_name=_('Текст блока 4'), blank=True, max_length=160, default='Текст блока 4. Краткое описание предлагаемых услуг')
    block5_title = models.CharField(verbose_name=_('Заголовок блока 5'), blank=True, max_length=50, default='Заголовок блока 5')
    block5_content = models.TextField(verbose_name=_('Текст блока 5'), blank=True, max_length=160, default='Текст блока 5. Краткое описание предлагаемых услуг')
    block6_title = models.CharField(verbose_name=_('Заголовок блока 6'), blank=True, max_length=50, default='Заголовок блока 6')
    block6_content = models.TextField(verbose_name=_('Текст блока 6'), blank=True, max_length=160, default='Текст блока 6. Краткое описание предлагаемых услуг')

    def __str__(self):
        return 'Настройка страницы "О нас" на главной странице'

    class Meta:
        verbose_name = _("О нас")
        verbose_name_plural = _("О нас")


class ContactsSettings(SingletonModel):
    phone1 = models.CharField(verbose_name=_('Телефон 1'), max_length=32, default='8 (495) 632-52-11')
    phone2 = models.CharField(verbose_name=_('Телефон 2'), max_length=32, blank=True, default='8 (495) 111-22-33')
    email = models.CharField(verbose_name=_('E-mail'), max_length=128, default='info@equimedia.ru')
    address = models.CharField(verbose_name=_('Адрес'), max_length=128, default='Московская область, Ленинский городской округ, сельское поселение Молоковское.')
    map = models.TextField(verbose_name=_('Карта'), max_length=1024, default='<a href="https://yandex.ru/maps/org/ksk_vivat_rossiya_/194812110432/?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:0px;">КСК Виват, Россия!</a><a href="https://yandex.ru/maps/1/moscow-and-moscow-oblast/category/horse_riding/184107287/?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:14px;">Конный клуб в Москве и Московской области</a><iframe src="https://yandex.ru/map-widget/v1/?ll=37.863109%2C55.553340&mode=search&oid=194812110432&ol=biz&utm_source=ntp_chrome&z=12.23" width="560" height="560" frameborder="1" allowfullscreen="true" style="position:relative;"></iframe>')
    poster_contacts = models.ImageField(upload_to='media/contacts/poster/%Y/%m/%d', default='images/contacts/contacts.webp',
                                        verbose_name=_('Обложка для раздела "Контакты"'))

    def __str__(self):
        return 'Настройка страницы "Контакты"'

    class Meta:
        verbose_name = _("Контакты")
        verbose_name_plural = _("Контакты")


class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name=_('Тема письма'))
    email = models.EmailField(max_length=255, verbose_name=_('Ваш электронный адрес (email)'))
    content = models.TextField(verbose_name=_('Содержимое письма'))
    time_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата отправки'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP отправителя'), blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Обратная связь')
        verbose_name_plural = _('Обратная связь')
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'Вам письмо от {self.email}'
