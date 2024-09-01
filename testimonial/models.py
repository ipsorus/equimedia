from django.db import models
from django.utils.translation import gettext_lazy as _


class Testimonial(models.Model):
    content = models.TextField(max_length=250, verbose_name=_("Текст отзыва"))
    author = models.CharField(max_length=100, verbose_name=_("Автор отзыва"))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP отправителя'), blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name=_("Email автора"))
    time_create = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания отзыва"))
    time_update = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления отзыва"))
    is_published = models.BooleanField(default=False, verbose_name=_("Публикация отзыва"))

    def __str__(self):
        return f'{self.author} - {self.content}'

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
