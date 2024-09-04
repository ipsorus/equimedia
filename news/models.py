from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from equi_media_portal.singleton import SingletonModel
from django.utils.translation import gettext_lazy as _

from equi_media_portal.utils import image_compress

User = get_user_model()


class NewsPost(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name=_("Заголовок новости"))
    content = CKEditor5Field(blank=True, verbose_name=_("Содержание новости"))
    image = models.ImageField(upload_to='media/news/%Y/%m/%d', blank=True, verbose_name=_("Постер для новости"))
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name=_("Публикация новости"))
    source_url = models.URLField(max_length=150, blank=True, verbose_name=_("Ссылка на источник новости"))
    source_text = models.CharField(max_length=200, blank=True, verbose_name=_("Текст ссылки на источник"))
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT, related_name='author_news_posts',
                               default=1)
    slider = models.BooleanField(default=False, verbose_name=_("Добавить новость в слайдер?"))

    def get_absolute_url(self):
        return reverse('news_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('news_post_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('news_post_delete', kwargs={'pk': self.id})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.image if self.pk else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__thumbnail != self.image and self.image:
            image_compress(self.image.path, width=1920, height=1080)

    def __str__(self):
        return f'Дата создания: {self.time_create} - {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_sum_rating(self):
        return sum([rating.value for rating in self.news_ratings.all()])

    def get_view_count(self):
        """
        Возвращает количество просмотров для данной статьи
        """
        return self.views_news.count()


class ViewCount(models.Model):
    """
    Модель просмотров для статей
    """
    news = models.ForeignKey('NewsPost', on_delete=models.CASCADE, related_name='views_news')
    ip_address = models.GenericIPAddressField(verbose_name=_('IP адрес'))
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата просмотра'))

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.news.title


class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, verbose_name=_('Новость'), related_name='comments_news')
    author = models.ForeignKey(User, verbose_name=_('Автор комментария'), on_delete=models.CASCADE,
                               related_name='comments_news_author')
    content = models.TextField(verbose_name=_('Текст комментария'), max_length=3000)
    time_create = models.DateTimeField(verbose_name=_('Время добавления'), auto_now_add=True)
    time_update = models.DateTimeField(verbose_name=_('Время обновления'), auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name=_('Статус комментария'), max_length=10)
    parent = TreeForeignKey('self', verbose_name=_('Родительский комментарий'), null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-time_create',)

    class Meta:
        indexes = [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'])]
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.content}'


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


class Rating(models.Model):
    """
    Модель рейтинга: Лайк - Дизлайк
    """
    post = models.ForeignKey(to=NewsPost, verbose_name=_('Статья'), on_delete=models.CASCADE, related_name='news_ratings')
    user = models.ForeignKey(to=User, verbose_name=_('Пользователь'), on_delete=models.CASCADE, blank=True, null=True, related_name='news_user')
    value = models.IntegerField(verbose_name=_('Значение'), choices=[(1, 'Нравится'), (-1, 'Не нравится')])
    time_create = models.DateTimeField(verbose_name=_('Время добавления'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Адрес'))

    class Meta:
        unique_together = ('post', 'ip_address')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create', 'value'])]
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.post.title
