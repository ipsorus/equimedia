import re
from sorl.thumbnail import ImageField, get_thumbnail
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from equi_media_portal.singleton import SingletonModel
from equi_media_portal.utils import image_compress

User = get_user_model()


class Video(models.Model):
    title = models.CharField(max_length=45, db_index=True, verbose_name=_("Заголовок видео"))
    video_link = models.TextField(verbose_name=_("Код видео (iframe) или ссылка на youtube, vk"))
    image = models.ImageField(upload_to='media/podcast/%Y/%m/%d', default='images/podcast/podcast.jpg', blank=True,
                              verbose_name=_("Постер для видео"))
    short = models.TextField(max_length=80, blank=True, verbose_name=_("Краткое описание"))
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name=_("Публикация видео"))
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT,
                               related_name='author_video',
                               default=1)

    def get_absolute_url(self):
        return reverse('video_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('video_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('video_delete', kwargs={'pk': self.id})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.image if self.pk else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__thumbnail != self.image and self.image:
            image_compress(self.image.path, width=800, height=600)

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
            if 'vk.com' in src_value:
                return src_value
            else:
                src_value = src_value.replace('embed/', '?v=')
                return src_value
        else:
            pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|vk\.com)/(watch\?v=|\?v=|video\?z=video|video|live\/)?([^&]+)"
            result = re.findall(pattern, str(self.video_link))
            if 'vk' in str(self.video_link):
                res = result[0][-1].split('_')
                return f'https://vk.com/video_ext.php?oid={res[0]}&id={res[1]}&hd=1&autoplay=0'
            elif 'yout' in str(self.video_link):
                return f'https://www.youtube.com/?v={result[0][-1]}'
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
