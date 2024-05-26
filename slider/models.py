from django.db import models


class Slider(models.Model):
    title = models.TextField(max_length=200, db_index=True, verbose_name="Заголовок слайда")
    url = models.CharField(max_length=350, verbose_name="Ссылка в слайде")
    additional_content = models.TextField(max_length=250, blank=True, verbose_name="Дополнительный текст слайда")
    poster = models.ImageField(upload_to='media/slider/poster/%Y/%m/%d', verbose_name="Обложка слайда")
    video = models.FileField(upload_to='media/slider/video/%Y/%m/%d', blank=True, verbose_name="Видео слайд")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания слайда")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления слайда")
    is_published = models.BooleanField(default=False, verbose_name="Публикация слайда")
    is_video = models.BooleanField(default=False, verbose_name="Слайд с видео-контентом")

    def __str__(self):
        return f'{self.title}, {self.additional_content}'

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
