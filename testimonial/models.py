from django.db import models
from django.urls import reverse


class Testimonial(models.Model):
    content = models.CharField(max_length=250, verbose_name="Текст отзыва")
    # slug = models.SlugField(max_length=150, unique=True, db_index=True)
    author = models.CharField(max_length=100, verbose_name="Автор отзыва")
    email = models.EmailField(max_length=100, verbose_name="Email автора")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания отзыва")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления отзыва")
    is_published = models.BooleanField(default=False, verbose_name="Публикация отзыва")
    #
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
        return f'{self.content}'

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
