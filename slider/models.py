from django.db import models
from django.urls import reverse

from equi_media_portal.singleton import SingletonModel
from django.utils.translation import gettext_lazy as _

from equi_media_portal.utils import image_compress


class Slider(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name=_("Заголовок слайда"))
    url = models.CharField(max_length=350, verbose_name=_("Ссылка в слайде"))
    additional_content = models.TextField(max_length=250, blank=True, verbose_name=_("Дополнительный текст слайда"))
    poster = models.ImageField(upload_to='media/slider/poster/%Y/%m/%d', verbose_name=_("Обложка слайда"))
    video = models.FileField(upload_to='media/slider/video/%Y/%m/%d', blank=True, verbose_name=_("Видео слайд"))
    time_create = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания слайда"))
    time_update = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления слайда"))
    is_published = models.BooleanField(default=False, verbose_name=_("Публикация слайда"))
    is_video = models.BooleanField(default=False, verbose_name=_("Слайд с видео-контентом"))
    third_party_site = models.BooleanField(default=False, verbose_name=_("Ссылка на сторонний сайт, откроется в новом окне"))

    def get_update_url(self):
        return reverse('slide_update_url', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('slide_delete_url', kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.title}, {self.additional_content}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.poster if self.pk else None

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__thumbnail != self.poster and self.poster:
            image_compress(self.poster.path, width=3840, height=2400)


class SliderSettings(SingletonModel):
    announcement_slider = models.BooleanField(verbose_name=_('Анонс новостей в слайдере'), default=True)
    pagination_dots = models.BooleanField(verbose_name=_('Пагинатор на слайдере'), default=True)
    scroller = models.BooleanField(verbose_name=_('Анимация скролла на слайдере'), default=True)

    def __str__(self):
        return 'Основные настройки блока "Слайдер"'

    class Meta:
        verbose_name = "Настройки раздела"
        verbose_name_plural = "Настройки раздела"
