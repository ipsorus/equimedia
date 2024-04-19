from ckeditor.fields import RichTextField
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Заголовок новости")
    content = RichTextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name="Публикация записи")
    category = models.ManyToManyField('Category', default=1, related_name='posts', verbose_name="Категории")

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    title = models.CharField(max_length=30, db_index=True, verbose_name="Название категории")

    def __str__(self):
        return f'{self.title}'
