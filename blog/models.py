from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

from equi_media_portal.singleton import SingletonModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BlogPost(models.Model):
    """
    Модель постов для сайта
    """

    class BlogPostManager(models.Manager):
        """
        Кастомный менеджер для модели статей
        """

        def all(self):
            """
            Список статей (SQL запрос с фильтрацией для страницы списка статей)
            """
            return self.get_queryset().select_related('author').filter(is_published=True)

        def detail(self):
            """
            Детальная статья (SQL запрос с фильтрацией для страницы со статьёй)
            """
            return self.get_queryset() \
                .select_related('author') \
                .prefetch_related('comments', 'comments__author') \
                .filter(is_published=True)

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    content = CKEditor5Field(verbose_name='Содержание поста')
    thumbnail = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    is_published = models.BooleanField(default=False, verbose_name="Публикация новости")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts',
                               default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блогов'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        super().save(*args, **kwargs)


class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, verbose_name='Запись блога', related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
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


class BlogSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название блока на главной странице'), max_length=64, default='Блоги')
    title_blog_page = models.CharField(verbose_name=_('Название в разделе "Блоги"'), max_length=128, blank=True, default='Блоги')
    sub_title_blog_page = models.CharField(verbose_name=_('Текст под названием в разделе "Блоги"'), max_length=128,
                                           blank=True, default='Истории наших пользователей о лошадях и не только...')
    last_comments = models.BooleanField(verbose_name=_('Последние комментарии в блогах'), default=True)
    recent_posts = models.BooleanField(verbose_name=_('Блок "Может быть интересно" в блогах'), default=True)
    sidebar_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32, default='Рекомендуем')
    posts_on_page = models.IntegerField(verbose_name=_('Количество видимых постов без скроллинга'), default=6)

    def __str__(self):
        return 'Основные настройки блока "Блоги"'

    class Meta:
        verbose_name = "Настройки раздела"
        verbose_name_plural = "Настройки раздела"


class BannerBlogSidebar(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер в сайдбаре #1 (ширина 300px)'
        verbose_name_plural = 'Баннер в сайдбаре #1  (ширина 300px)'


class BannerBlogSidebar2(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png', verbose_name='Обложка для рекламного блока')
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return 'Настроить баннер'

    class Meta:
        verbose_name = 'Баннер в сайдбаре #2 (ширина 300px)'
        verbose_name_plural = 'Баннер в сайдбаре #2 (ширина 300px)'
