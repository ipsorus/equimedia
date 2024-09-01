import json
from datetime import timedelta, datetime
from itertools import chain
from operator import attrgetter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from event.forms import EventUpdateForm, EventCreateForm, EventDocumentCreateForm, TournamentDocumentCreateForm, \
    TournamentCreateForm, TournamentUpdateForm, TournamentStageCreateForm, StageUpdateForm, StageDocumentCreateForm, \
    TournamentCloseForm, TournamentDocumentCloseForm, StageDocumentCloseForm, StageCloseForm
from event.models import Event, Tournament, Stage, EventDocument, TournamentDocument, StageDocument, \
    TournamentCloseDocument, StageCloseDocument
from services.mixins import AuthorRequiredMixin
from django.forms.models import inlineformset_factory


def event_detail(request, event_id):
    single_event = get_object_or_404(Event, pk=event_id)
    documents = EventDocument.objects.filter(event=event_id)
    other_events = Event.objects.filter(is_published=True).exclude(pk=single_event.id)[:5]

    return render(request, 'event/event_detail.html', {'item': single_event,
                                                       'documents': documents,
                                                       'other_events': other_events})


def calendar_view(request):
    events = Event.objects.filter(is_published=True).values('date_start', 'date_end')
    stages = Stage.objects.filter(is_published=True).values('date_start', 'date_end')
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True).values('date_start', 'date_end')
    result_list = list(chain(events, stages, tournaments))

    dates = set()
    for event in result_list:
        if event:
            start_date = event['date_start']
            dates.add(start_date)
            if event['date_end']:
                end_date = event['date_end']
                delta = (end_date - start_date).days
                dates.add(end_date)
                for i in range(int(delta) + 1):
                    dates.add(start_date + timedelta(days=i))

    return render(request, 'event/calendar.html', {'events': dates, 'title': 'Календарь мероприятий'})


def get_events(request):
    date = json.loads(request.GET.get('date'))
    date_ = datetime.strptime(f'{date["month"]}.{date["day"]}.{date["year"]}', '%m.%d.%Y').date()
    events = Event.objects.filter(is_published=True, date_start__lte=date_, date_end__gte=date_)
    stages = Stage.objects.filter(is_published=True, date_start__lte=date_, date_end__gte=date_)
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__lte=date_,
                                            date_end__gte=date_)
    result_list = sorted(list(chain(events, stages, tournaments)), key=attrgetter('date_start'))

    return render(request, 'event/events_by_date.html',
                  {'events': result_list, 'date': date_, 'day_name': date['weekdayname']})


def get_weekly_events(request):
    date = json.loads(request.GET.get('date'))
    date_ = datetime.strptime(f'{date["month"]}.{date["day"]}.{date["year"]}', '%m.%d.%Y').date()
    week_start = date_ - timedelta(days=date['weekday'])
    week_end = week_start + timedelta(days=6)
    events = Event.objects.filter(is_published=True, date_start__range=[week_start, week_end])
    stages = Stage.objects.filter(is_published=True, date_start__range=[week_start, week_end])
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True,
                                            date_start__range=[week_start, week_end])

    result_list = sorted(list(chain(events, stages, tournaments)), key=attrgetter('date_start'))

    return render(request, 'event/events_by_week.html', {'events': result_list})


def get_monthly_events(request):
    events_dict = {}
    dates = json.loads(request.GET.get('dates'))
    month = dates.pop('month')
    year = dates.pop('year')
    for week in dates.keys():
        last_month = month
        other_year = year
        first_day = int(dates[week][0])
        last_day = int(dates[week][-1])

        week_start = datetime.strptime(f'{month}.{first_day}.{year}', '%m.%d.%Y').date()
        week_end = datetime.strptime(f'{month}.{last_day}.{year}', '%m.%d.%Y').date()

        if int(week) == 1 and first_day > last_day:
            if month == 1:
                last_month = 12
                other_year -= 1
            elif 12 >= month >= 2:
                last_month -= 1

            week_start = datetime.strptime(f'{last_month}.{first_day}.{other_year}', '%m.%d.%Y').date()
            week_end = datetime.strptime(f'{month}.{last_day}.{year}', '%m.%d.%Y').date()

        elif int(week) >= 5 and last_day < first_day:
            if month == 12:
                last_month = 1
                other_year += 1
            elif 11 >= month >= 1:
                last_month += 1

            week_start = datetime.strptime(f'{month}.{first_day}.{year}', '%m.%d.%Y').date()
            week_end = datetime.strptime(f'{last_month}.{last_day}.{year}', '%m.%d.%Y').date()

        events = Event.objects.filter(is_published=True, date_start__range=[week_start, week_end])
        stages = Stage.objects.filter(is_published=True, date_start__range=[week_start, week_end])
        tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True,
                                                date_start__range=[week_start, week_end])
        result_list = sorted(list(chain(events, stages, tournaments)), key=attrgetter('date_start'))

        events_dict[week] = dict(first=week_start, last=week_end, items=result_list)

    return render(request, 'event/events_by_month.html', {'events': events_dict})


def tournaments(request):
    tournaments_list = Tournament.objects.all()
    return render(request, 'event/tournaments.html', {'tournaments': tournaments_list, 'title': 'Турниры'})


def tournament_detail(request, tournament_id):
    single_tournament = get_object_or_404(Tournament, pk=tournament_id)
    stages = Stage.objects.filter(is_published=True, tournament=single_tournament.id)
    documents = TournamentDocument.objects.filter(tournament=tournament_id)
    documents_close = TournamentCloseDocument.objects.filter(tournament=tournament_id)
    other_tournaments = Tournament.objects.filter(is_published=True).exclude(pk=single_tournament.id)[:5]

    return render(request, 'event/tournament_detail.html', {'item': single_tournament,
                                                            'stages': stages,
                                                            'title': single_tournament.title,
                                                            'documents': documents,
                                                            'documents_close': documents_close,
                                                            'other_tournaments': other_tournaments
                                                            })


def contest_detail(request, tournament_id):
    single_tournament = get_object_or_404(Tournament, pk=tournament_id, stages__isnull=True)
    documents = TournamentDocument.objects.filter(tournament=tournament_id)
    documents_close = TournamentCloseDocument.objects.filter(tournament=tournament_id)
    other_tournaments = Tournament.objects.filter(is_published=True).exclude(pk=single_tournament.id)[:5]

    return render(request, 'event/contest_detail.html', {'item': single_tournament,
                                                         'title': single_tournament.title,
                                                         'documents': documents,
                                                         'documents_close': documents_close,
                                                         'other_tournaments': other_tournaments
                                                         })


def stage_detail(request, tournament_id, stage_id):
    single_stage = get_object_or_404(Stage, pk=stage_id)
    documents = StageDocument.objects.filter(stage=stage_id)
    documents_close = StageCloseDocument.objects.filter(stage=stage_id)
    other_stages = Stage.objects.filter(is_published=True, tournament_id=tournament_id).exclude(pk=single_stage.id)
    return render(request, 'event/stage_detail.html', {'item': single_stage,
                                                       'title': single_stage.title,
                                                       'documents': documents,
                                                       'documents_close': documents_close,
                                                       'other_stages': other_stages})


# special field names
TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = 'ORDER'
DELETION_FIELD_NAME = 'DELETE'

# default minimum number of forms in a formset
DEFAULT_MIN_NUM = 0

# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 10

EventDocumentFormset = inlineformset_factory(
    Event, EventDocument, form=EventDocumentCreateForm, fields='__all__', extra=1, can_delete=True,
    max_num=DEFAULT_MAX_NUM, min_num=DEFAULT_MIN_NUM, can_delete_extra=False
)


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Event
    template_name = 'event/event-create.html'
    form_class = EventCreateForm
    login_url = 'event_detail_url'
    success_message = 'Материал был успешно добавлен'

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super(EventCreateView, self).get_context_data(**kwargs)
        data['title'] = 'Добавление события на сайт'

        if self.request.POST:
            data["document_form"] = EventDocumentFormset(self.request.POST, self.request.FILES)
        else:
            data["document_form"] = EventDocumentFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context['document_form']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()
        return super(EventCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_detail_url', kwargs={'event_id': self.object.pk})


class EventUpdateView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновление материала на сайте
    """
    model = Event
    template_name = 'event/event-update.html'
    context_object_name = 'item'
    form_class = EventUpdateForm
    login_url = 'main'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, **kwargs):
        data = super(EventUpdateView, self).get_context_data(**kwargs)
        data['title'] = f'Обновление записи: {self.object.title}'
        if self.request.POST:
            data["document_form"] = EventDocumentFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data["document_form"] = EventDocumentFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context["document_form"]
        with transaction.atomic():
            self.object = form.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()
        return super(EventUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_detail_url', kwargs={'event_id': self.object.pk})


class EventDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Event
    success_url = reverse_lazy('calendar_page')
    context_object_name = 'post'
    template_name = 'event/event-delete.html'
    success_message = 'Событие было успешно удалено'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context


TournamentDocumentFormset = inlineformset_factory(
    Tournament, TournamentDocument, form=TournamentDocumentCreateForm, fields='__all__', extra=1, can_delete=True,
    max_num=DEFAULT_MAX_NUM, min_num=DEFAULT_MIN_NUM, can_delete_extra=False
)

StageFormset = inlineformset_factory(
    Tournament, Stage, form=TournamentStageCreateForm, fields='__all__', extra=1, can_delete=True,
    max_num=DEFAULT_MAX_NUM, min_num=DEFAULT_MIN_NUM, can_delete_extra=False
)

StageDocumentFormset = inlineformset_factory(
    Stage, StageDocument, form=StageDocumentCreateForm, fields='__all__', extra=1, can_delete=True,
    max_num=DEFAULT_MAX_NUM, min_num=DEFAULT_MIN_NUM, can_delete_extra=False
)

TournamentCloseDocumentFormset = inlineformset_factory(
    Tournament, TournamentCloseDocument, form=TournamentDocumentCloseForm, fields='__all__', extra=1, can_delete=True,
    max_num=DEFAULT_MAX_NUM, min_num=DEFAULT_MIN_NUM, can_delete_extra=False
)

StageCloseDocumentFormset = inlineformset_factory(
    Stage, StageCloseDocument, form=StageDocumentCloseForm, fields='__all__', extra=1, can_delete=True,
    max_num=DEFAULT_MAX_NUM, min_num=DEFAULT_MIN_NUM, can_delete_extra=False
)


class TournamentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Tournament
    template_name = 'event/tournament-create.html'
    form_class = TournamentCreateForm
    login_url = 'tournament_detail_url'
    success_message = 'Турнир был успешно добавлен'

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super(TournamentCreateView, self).get_context_data(**kwargs)
        data['title'] = 'Добавление турнира на сайт'

        if self.request.POST:
            data["document_form"] = TournamentDocumentFormset(self.request.POST, self.request.FILES)
            data["stage_form"] = StageFormset(self.request.POST, self.request.FILES)
        else:
            data["document_form"] = TournamentDocumentFormset()
            data["stage_form"] = StageFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context['document_form']
        stages = context['stage_form']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()
            if stages.is_valid():
                stages.instance = self.object
                stages.save()
        return super(TournamentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tournament_detail_url', kwargs={'tournament_id': self.object.pk})


class TournamentUpdateView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновление турнира на сайте
    """
    model = Tournament
    template_name = 'event/tournament-update.html'
    context_object_name = 'item'
    form_class = TournamentUpdateForm
    login_url = 'main'
    success_message = 'Турнир был успешно обновлен'

    def get_context_data(self, **kwargs):
        data = super(TournamentUpdateView, self).get_context_data(**kwargs)
        data['title'] = f'Обновление турнира: {self.object.title}'
        if self.request.POST:
            data["document_form"] = TournamentDocumentFormset(self.request.POST, self.request.FILES,
                                                              instance=self.object)
            data["stage_form"] = StageFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data["document_form"] = TournamentDocumentFormset(instance=self.object)
            data["stage_form"] = StageFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context["document_form"]
        stages = context['stage_form']
        with transaction.atomic():
            self.object = form.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()
            if stages.is_valid():
                stages.instance = self.object
                stages.save()
        return super(TournamentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tournament_detail_url', kwargs={'tournament_id': self.object.pk})


class TournamentDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления турнира
    """
    model = Tournament
    success_url = reverse_lazy('calendar_page')
    context_object_name = 'post'
    template_name = 'event/tournament-delete.html'
    success_message = 'Турнир был успешно удален'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление турнира: {self.object.title}'
        return context


class StageUpdateView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновление этапа турнира на сайте
    """
    model = Stage
    template_name = 'event/stage-update.html'
    context_object_name = 'item'
    form_class = StageUpdateForm
    login_url = 'main'
    success_message = 'Этап турнира был успешно обновлен'

    def get_context_data(self, **kwargs):
        data = super(StageUpdateView, self).get_context_data(**kwargs)
        data['title'] = f'Обновление этапа турнира: {self.object.title}'
        if self.request.POST:
            data["document_form"] = StageDocumentFormset(self.request.POST, self.request.FILES,
                                                         instance=self.object)
        else:
            data["document_form"] = StageDocumentFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context["document_form"]
        with transaction.atomic():
            self.object = form.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()

        return super(StageUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('stage_detail_url',
                            kwargs={'tournament_id': self.object.tournament.pk, 'stage_id': self.object.pk})


class StageDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления турнира
    """
    model = Stage
    success_url = reverse_lazy('calendar_page')
    context_object_name = 'post'
    template_name = 'event/stage-delete.html'
    success_message = 'Этап турнира был успешно удален'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление этапа турнира: {self.object.title}'
        return context


class TournamentCloseView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: завершение турнира на сайте
    """
    model = Tournament
    template_name = 'event/tournament-close.html'
    context_object_name = 'item'
    form_class = TournamentCloseForm
    login_url = 'main'
    success_message = 'Турнир успешно завершен'

    def get_context_data(self, **kwargs):
        data = super(TournamentCloseView, self).get_context_data(**kwargs)
        data['title'] = f'Подведение итогов турнира: {self.object.title}'
        if self.request.POST:
            data["document_close_form"] = TournamentCloseDocumentFormset(self.request.POST, self.request.FILES,
                                                                         instance=self.object)
        else:
            data["document_close_form"] = TournamentCloseDocumentFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context["document_close_form"]
        with transaction.atomic():
            self.object = form.save()
            stages = self.object.stages.all()
            for stage in stages:
                stage.is_closed = True
                stage.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()

        return super(TournamentCloseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tournament_detail_url', kwargs={'tournament_id': self.object.pk})


class StageCloseView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: завершение этапа турнира на сайте
    """
    model = Stage
    template_name = 'event/stage-close.html'
    context_object_name = 'item'
    form_class = StageCloseForm
    login_url = 'main'
    success_message = 'Этап турнира успешно завершен'

    def get_context_data(self, **kwargs):
        data = super(StageCloseView, self).get_context_data(**kwargs)
        data['title'] = f'Подведение итогов этапа турнира: {self.object.title}'
        if self.request.POST:
            data["document_stage_close_form"] = StageCloseDocumentFormset(self.request.POST, self.request.FILES,
                                                                          instance=self.object)
        else:
            data["document_stage_close_form"] = StageCloseDocumentFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context["document_stage_close_form"]
        with transaction.atomic():
            self.object = form.save()
            if documents.is_valid():
                documents.instance = self.object
                documents.save()

        return super(StageCloseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('stage_detail_url',
                            kwargs={'tournament_id': self.object.tournament.pk, 'stage_id': self.object.pk})
