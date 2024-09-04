import os

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from equi_media_portal.singleton import SingletonModel
from django.utils.translation import gettext_lazy as _

from equi_media_portal.utils import image_compress

User = get_user_model()


class Discipline(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название дисциплины"))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Дисциплина')
        verbose_name_plural = _('Дисциплины')


class EventType(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Тип события"))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Тип события')
        verbose_name_plural = _('Типы событий')


class ContestType(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Уровень события"))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Уровень события')
        verbose_name_plural = _('Уровни событий')


class StageType(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name=_("Тип этапа соревнования"))

    def __str__(self):
        return f'{self.title}'


class Tournament(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name=_("Название турнира"))
    image = models.ImageField(upload_to='media/tournaments/%Y/%m/%d', blank=True, verbose_name=_("Постер для турнира"))
    location = models.TextField(max_length=300, verbose_name=_("Место проведения"))
    discipline = models.ManyToManyField(Discipline, max_length=100, verbose_name=_('Дисциплина'))
    type = models.ForeignKey(ContestType, on_delete=models.PROTECT, max_length=100, verbose_name=_('Уровень соревнования'))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    result = CKEditor5Field(max_length=1000, blank=True, verbose_name=_("Результаты турнира"))
    prize = CKEditor5Field(max_length=300, blank=True, verbose_name=_("Призовой фонд"))
    description = CKEditor5Field(blank=True, verbose_name=_("Описание и условия турнира"))
    is_published = models.BooleanField(default=False, verbose_name=_("Опубликовать запись"))
    is_closed = models.BooleanField(default=False, verbose_name=_("Турнир завершен"))
    time_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT,
                               related_name='author_tournament',
                               default=1)

    def get_absolute_url(self):
        return reverse('tournament_detail_url', kwargs={'tournament_id': self.id})

    def get_update_url(self):
        return reverse('tournament_update_url', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('tournament_delete_url', kwargs={'pk': self.id})

    def get_close_url(self):
        return reverse('tournament_close_url', kwargs={'pk': self.id})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.image if self.pk else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__thumbnail != self.image and self.image:
            image_compress(self.image.path, width=1920, height=1080)

    def __str__(self):
        return f'{self.title, self.date_start}'

    class Meta:
        verbose_name = _('Турнир')
        verbose_name_plural = _('Турниры')
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['date_start'])
        ]


class TournamentDocument(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="tournament_doc")
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название документа"))
    file = models.FileField(upload_to='media/documents/tournaments/%Y/%m/%d', verbose_name=_("Файл"))
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lstrip('.')

    class Meta:
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')


class TournamentCloseDocument(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="tournament_close_doc")
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название документа"))
    file = models.FileField(upload_to='media/documents/tournaments/%Y/%m/%d', verbose_name=_("Файл"))
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lstrip('.')

    class Meta:
        verbose_name = _('Документ с результатами')
        verbose_name_plural = _('Документы с результатами')


class Stage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="stages", verbose_name=_('Турнир'))
    stage_type = models.CharField(max_length=100, default='Соревнования', verbose_name=_('Тип соревнования'))
    type = models.ForeignKey(ContestType, on_delete=models.PROTECT, max_length=100, verbose_name=_('Уровень соревнования'))
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название этапа турнира"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    location = models.TextField(max_length=300, verbose_name=_("Место проведения"))
    discipline = models.ManyToManyField(Discipline, max_length=100, verbose_name=_('Дисциплина'))
    prize = CKEditor5Field(max_length=300, blank=True, verbose_name=_("Призовой фонд"))
    result = CKEditor5Field(max_length=1000, blank=True, verbose_name=_("Результаты соревнования"))
    description = CKEditor5Field(max_length=2000, blank=True, verbose_name=_("Описание и программа"))
    is_published = models.BooleanField(default=True, verbose_name=_("Опубликовать запись"))
    is_closed = models.BooleanField(default=False, verbose_name=_("Этап завершен"))
    time_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT, related_name='author_stage',
                               default=1)

    def get_absolute_url(self):
        return reverse('stage_detail_url', kwargs={'stage_id': self.id})

    def get_update_url(self):
        return reverse('stage_update_url', kwargs={'tournament_id': self.tournament.id, 'pk': self.id})

    def get_delete_url(self):
        return reverse('stage_delete_url', kwargs={'tournament_id': self.tournament.id, 'pk': self.id})

    def get_close_url(self):
        return reverse('stage_close_url', kwargs={'tournament_id': self.tournament.id, 'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title, self.date_start}'

    class Meta:
        verbose_name = _('Этап турнира')
        verbose_name_plural = _('Этапы турнира')
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['date_start'])
        ]


class StageDocument(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="stage")
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название документа"))
    file = models.FileField(upload_to='media/documents/stage/%Y/%m/%d', verbose_name=_("Файл"))
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lstrip('.')

    class Meta:
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')


class StageCloseDocument(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="stage_close_doc")
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название документа"))
    file = models.FileField(upload_to='media/documents/tournaments/stages/%Y/%m/%d', verbose_name=_("Файл"))
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lstrip('.')

    class Meta:
        verbose_name = _('Документ с результатами')
        verbose_name_plural = _('Документы с результатами')


class Event(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название события"))
    event_type = models.ForeignKey(EventType, on_delete=models.PROTECT, max_length=100, verbose_name=_('Тип события'))
    type = models.ForeignKey(ContestType, on_delete=models.PROTECT, max_length=100, verbose_name=_('Уровень мероприятия'))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    location = models.TextField(max_length=300, verbose_name=_("Место проведения"))
    image = models.ImageField(upload_to='media/events/%Y/%m/%d', verbose_name=_("Постер для события"))
    description = CKEditor5Field(max_length=2000, blank=True, verbose_name=_("Краткое описание"))
    is_published = models.BooleanField(default=False, verbose_name=_("Опубликовать запись"))
    time_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, verbose_name=_('Автор'), on_delete=models.SET_DEFAULT, related_name='author_event',
                               default=1)

    def get_absolute_url(self):
        return reverse('event_detail_url', kwargs={'event_id': self.id})

    def get_update_url(self):
        return reverse('event_update_url', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('event_delete_url', kwargs={'pk': self.id})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.image if self.pk else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__thumbnail != self.image and self.image:
            image_compress(self.image.path, width=1920, height=1080)

    def __str__(self):
        return f'{self.title, self.date_start}'

    class Meta:
        verbose_name = _('Событие')
        verbose_name_plural = _('События')
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['date_start'])
        ]


class EventDocument(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("Название документа"))
    file = models.FileField(upload_to='media/documents/events/%Y/%m/%d', verbose_name=_("Файл"))
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lstrip('.')

    class Meta:
        verbose_name = _('Документ')
        verbose_name_plural = _('Документы')


class EventSettings(SingletonModel):
    title = models.CharField(verbose_name=_('Название раздела'), max_length=128, default='События')
    sub_title = models.CharField(verbose_name=_('Текст под названием в разделе "События"'), max_length=128,
                                 blank=True, default='Не пропустите важные события и мероприятия')
    sticky_sidebar = models.BooleanField(verbose_name=_('Подвижный сайдбар в событиях'), default=True)
    other_events_sidebar = models.BooleanField(verbose_name=_('Другие события в сайдбаре карточки события'), default=True)
    other_events_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32, default='Другие события')
    adv_events_title = models.CharField(verbose_name=_('Заголовок для сайдбара'), max_length=32, default='Рекомендуем')

    def __str__(self):
        return _('Основные настройки блока "События"')

    class Meta:
        verbose_name = _("Настройки раздела")
        verbose_name_plural = _("Настройки раздела")


class BannerEventSideBar1(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png',
                               verbose_name=_('Обложка для рекламного блока'))
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return _('Настроить баннер')

    class Meta:
        verbose_name = _('Баннер в сайдбаре #1 (ширина 300px)')
        verbose_name_plural = _('Баннер в сайдбаре #1 (ширина 300px)')


class BannerEventSideBar2(SingletonModel):
    url = models.URLField(verbose_name=_('Адрес сайта'), max_length=256, blank=True)
    title = models.CharField(verbose_name=_('Альтернативное название постера'), max_length=256, default='test')
    poster = models.ImageField(upload_to='media/adv/poster/%Y/%m/%d', default='images/adv/ad-blank.png',
                               verbose_name=_('Обложка для рекламного блока'))
    show = models.BooleanField(verbose_name=_('Показать баннер'), default=True)

    def __str__(self):
        return _('Настроить баннер')

    class Meta:
        verbose_name = _('Баннер в сайдбаре #2 (ширина 300px)')
        verbose_name_plural = _('Баннер в сайдбаре #2 (ширина 300px)')
