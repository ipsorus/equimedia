from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок новости")
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    content = RichTextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name="Публикация записи")

    def get_absolute_url(self):
        return reverse('news_detail_url', kwargs={'news_slug': self.slug})

    def get_update_url(self):
        return reverse('news_update_url', kwargs={'news_slug': self.slug})

    def get_delete_url(self):
        return reverse('news_delete_url', kwargs={'news_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок статьи")
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    content = RichTextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name="Публикация записи")

    def get_absolute_url(self):
        return reverse('article_detail_url', kwargs={'article_slug': self.slug})

    def get_update_url(self):
        return reverse('article_update_url', kwargs={'article_slug': self.slug})

    def get_delete_url(self):
        return reverse('article_delete_url', kwargs={'article_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class Category(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name="Название категории")

    def __str__(self):
        return f'{self.title}'
