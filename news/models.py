from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class NewsPost(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок новости")
    content = CKEditor5Field(blank=True, verbose_name="Содержание новости")
    image = models.ImageField(upload_to='media/news/%Y/%m/%d', blank=True, verbose_name="Постер для новости")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name="Публикация новости")
    source = models.CharField(max_length=150, blank=True, verbose_name="Источник новости")
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_news_posts',
                               default=1)

    def get_absolute_url(self):
        return reverse('news_detail_url', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('news_post_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('news_post_delete', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Дата создания: {self.time_create} - {self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
