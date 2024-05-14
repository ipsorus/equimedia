from django.db import models
from django.urls import reverse


class Slider(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок слайда")
    url = models.CharField(max_length=350, verbose_name="Ссылка в слайде")
    additional_content = models.CharField(max_length=100, blank=True, verbose_name="Дополнительный текст слайда")
    poster = models.ImageField(upload_to='media/slider/poster/%Y/%m/%d', verbose_name="Обложка слайда")
    video = models.FileField(upload_to='media/slider/video/%Y/%m/%d', blank=True, verbose_name="Видео слайд")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания слайда")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления слайда")
    is_published = models.BooleanField(default=False, verbose_name="Публикация слайда")
    is_video = models.BooleanField(default=False, verbose_name="Слайд с видео-контентом")

    # def get_absolute_url(self):
    #     return reverse('slider_detail_url', kwargs={'slider_slug': self.slug})
    #
    # def get_update_url(self):
    #     return reverse('slider_update_url', kwargs={'slider_slug': self.slug})
    #
    # def get_delete_url(self):
    #     return reverse('slider_delete_url', kwargs={'slider_slug': self.slug})
    #
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
