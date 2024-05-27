from django.db import models


class Testimonial(models.Model):
    content = models.TextField(max_length=250, verbose_name="Текст отзыва")
    author = models.CharField(max_length=100, verbose_name="Автор отзыва")
    email = models.EmailField(max_length=100, verbose_name="Email автора")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания отзыва")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления отзыва")
    is_published = models.BooleanField(default=False, verbose_name="Публикация отзыва")

    def __str__(self):
        return f'{self.author} - {self.content}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
