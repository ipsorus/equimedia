import re
from sorl.thumbnail import ImageField, get_thumbnail
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from equi_media_portal.singleton import SingletonModel

User = get_user_model()


class Video(models.Model):
    title = models.CharField(max_length=45, db_index=True, verbose_name=_("Заголовок видео"))
    video_link = models.TextField(verbose_name=_("Код видео (iframe) youtube, vk"))
    image = models.ImageField(upload_to='media/podcast/%Y/%m/%d', default='images/podcast/podcast.jpg', blank=True,
                              verbose_name=_("Постер для видео"))
    short = models.TextField(max_length=80, blank=True, verbose_name=_("Краткое описание"))
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name=_("Публикация видео"))
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT,
                               related_name='author_video',
                               default=1)

    # def get_absolute_url(self):
    #     return reverse('video_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('video_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('video_delete', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Дата создания: {self.time_create} - {self.title}'

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_cleaned_url(self):
        src_pattern = re.compile(r'<iframe.*?src="(.*?)"')
        src_match = src_pattern.search(str(self.video_link))

        if src_match:
            src_value = src_match.group(1)
            url = src_value.replace('embed/', '?v=')
            return url
        else:
            return self.video_link


class VideoSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название раздела на главной странице'), max_length=128,
                             default='Видео и подкасты')
    title_video_page = models.CharField(verbose_name=_('Название в разделе "Видео и подкасты"'), max_length=128,
                                        blank=True,
                                        default='Видео и подкасты')
    sub_title_video_page = models.CharField(verbose_name=_('Текст под названием в разделе "Видео и подкасты"'),
                                            max_length=128,
                                            blank=True, default='Интервью и репортажи')
    videos_on_page = models.IntegerField(verbose_name=_('Количество видимых видеоблоков без скроллинга'), default=6)

    def __str__(self):
        return 'Основные настройки блока "Видео и подкасты"'

    class Meta:
        verbose_name = "Настройки раздела"
        verbose_name_plural = "Настройки раздела"
