from django.db import models
from django.urls import reverse

from equi_media_portal import settings


class Discipline(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название дисциплины")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class EventType(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Тип события")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'


class ContestType(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="Тип соревнования")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тип соревнования'
        verbose_name_plural = 'Типы соревнований'


class StageType(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name="Тип этапа соревнования")

    def __str__(self):
        return f'{self.title}'


class Tournament(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name="Название турнира")
    location = models.TextField(max_length=300, blank=True, verbose_name="Место проведения")
    prize = models.TextField(max_length=300, blank=True, verbose_name="Призовой фонд")
    discipline = models.ManyToManyField(Discipline, max_length=100, verbose_name='Дисциплина')
    type = models.ManyToManyField(ContestType, max_length=100, verbose_name='Вид соревнования')
    date_start = models.DateField(verbose_name="Дата начала")
    date_end = models.DateField(verbose_name="Дата окончания")
    result = models.TextField(blank=True, verbose_name="Результаты турнира")
    image = models.ImageField(upload_to='media/tournaments/%Y/%m/%d', blank=True, verbose_name="Постер для турнира")
    description = models.TextField(blank=True, verbose_name="Описание и условия турнира")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать запись")
    time_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('tournament_detail_url', kwargs={'tournament_id': self.id})

    def get_update_url(self):
        return reverse('tournament_update_url', kwargs={'tournament_id': self.id})

    def get_delete_url(self):
        return reverse('tournament_delete_url', kwargs={'tournament_id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title, self.date_start}'

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['date_start'])
        ]


class TournamentDocument(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT, related_name="tournament_doc")
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название документа")
    description = models.CharField(blank=True, verbose_name="Описание документа")
    file = models.FileField(upload_to='media/documents/tournaments/%Y/%m/%d', blank=True, verbose_name="Файл")
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Stage(models.Model):
    tournament = models.ForeignKey(Tournament, null=True, blank=True, on_delete=models.PROTECT, related_name="stages")
    stage_type = models.CharField(max_length=100, default='Соревнования', verbose_name='Тип соревнования')
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название этапа турнира")
    date_start = models.DateField(verbose_name="Дата начала")
    date_end = models.DateField(verbose_name="Дата окончания")
    location = models.TextField(max_length=300, blank=True, verbose_name="Место проведения")
    discipline = models.ManyToManyField(Discipline, max_length=100, verbose_name='Дисциплина')
    type = models.ManyToManyField(ContestType, max_length=100, verbose_name='Вид соревнования')
    prize = models.TextField(max_length=300, blank=True, verbose_name="Призовой фонд")
    result = models.TextField(max_length=500, blank=True, verbose_name="Результаты соревнования")
    description = models.TextField(max_length=2000, blank=True, verbose_name="Описание")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать запись")
    time_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('stage_detail_url', kwargs={'stage_id': self.id})

    def get_update_url(self):
        return reverse('stage_update_url', kwargs={'stage_id': self.id})

    def get_delete_url(self):
        return reverse('stage_delete_url', kwargs={'stage_id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title, self.date_start}'

    class Meta:
        verbose_name = 'Этап турнира'
        verbose_name_plural = 'Этапы турнира'
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['date_start'])
        ]


class StageDocument(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name="stage")
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название документа")
    description = models.CharField(blank=True, verbose_name="Описание документа")
    file = models.FileField(upload_to='media/documents/stage/%Y/%m/%d', blank=True, verbose_name="Файл")
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Event(models.Model):
    event_type = models.ManyToManyField(EventType, max_length=100, verbose_name='Тип события')
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название события")
    date_start = models.DateField(verbose_name="Дата начала")
    date_end = models.DateField(verbose_name="Дата окончания")
    location = models.TextField(max_length=300, blank=True, verbose_name="Место проведения")
    type = models.ManyToManyField(ContestType, max_length=100, verbose_name='Вид мероприятия')
    prize = models.TextField(max_length=300, blank=True, verbose_name="Призовой фонд")
    result = models.TextField(max_length=500, blank=True, verbose_name="Результаты соревнований")
    image = models.ImageField(upload_to='media/events/%Y/%m/%d', blank=True, verbose_name="Постер для события")
    description = models.TextField(max_length=2000, blank=True, verbose_name="Краткое описание")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать запись")
    time_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('event_detail_url', kwargs={'event_id': self.id})

    def get_update_url(self):
        return reverse('event_update_url', kwargs={'event_id': self.id})

    def get_delete_url(self):
        return reverse('event_delete_url', kwargs={'event_id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title, self.date_start}'

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['date_start']
        indexes = [
            models.Index(fields=['date_start'])
        ]


class EventDocument(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="event")
    title = models.CharField(max_length=200, db_index=True, verbose_name="Название документа")
    description = models.CharField(blank=True, verbose_name="Описание документа")
    file = models.FileField(upload_to='media/documents/events/%Y/%m/%d', blank=True, verbose_name="Файл")
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
