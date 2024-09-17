import re
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from equi_media_portal.singleton import SingletonModel
from equi_media_portal.utils import image_compress

User = get_user_model()


class Broadcast(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name=_("Заголовок трансляции"))
    broadcast_link = models.TextField(verbose_name=_("Код видео (iframe) или ссылка на youtube, vk"))
    image = models.ImageField(upload_to='media/broadcast/%Y/%m/%d', default='images/broadcast/broadcast.webp', blank=True,
                              verbose_name=_("Постер для трансляции"))
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    show_broadcast = models.BooleanField(default=True, verbose_name=_("Включить показ трансляции"))
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT,
                               related_name='author_broadcast',
                               default=1)

    def get_absolute_url(self):
        return reverse('broadcast_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('broadcast_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('broadcast_delete', kwargs={'pk': self.id})

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
        verbose_name = 'Трансляция'
        verbose_name_plural = 'Трансляции'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_cleaned_url(self):
        src_pattern = re.compile(r'<iframe.*?src="(.*?)"')
        src_match = src_pattern.search(str(self.broadcast_link))

        if src_match:
            src_value = src_match.group(1)
            if 'vk.com' in src_value:
                return src_value
            else:
                src_value = src_value.replace('embed/', '?v=')
                return src_value
        else:
            pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|vk\.com)/(watch\?v=|\?v=|video\?z=video|video|live\/)?([^&]+)"
            result = re.findall(pattern, str(self.broadcast_link))
            if 'vk' in str(self.broadcast_link):
                res = result[0][-1].split('_')
                return f'https://vk.com/video_ext.php?oid={res[0]}&id={res[1]}&hd=1&autoplay=0'
            elif 'yout' in str(self.broadcast_link):
                return f'https://www.youtube.com/?v={result[0][-1]}'
            else:
                return self.broadcast_link


class BroadcastSettings(SingletonModel):
    page_title = models.CharField(verbose_name=_('Название в разделе "Трансляции"'), max_length=128,
                                  default='Трансляции соревнований')
    sub_title_broadcast_page = models.CharField(verbose_name=_('Текст под названием в разделе "Трансляции"'),
                                                max_length=128,
                                                blank=True,
                                                default='Смотрите прямые трансляции и болейте за свою команду вместе с нами')

    def __str__(self):
        return 'Основные настройки блока "Трансляции"'

    class Meta:
        verbose_name = "Настройки раздела"
        verbose_name_plural = "Настройки раздела"
