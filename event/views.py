import json
from datetime import timedelta, datetime
from itertools import chain
from operator import attrgetter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from event.forms import EventUpdateForm, EventCreateForm
from event.models import Event, Tournament, Stage
from services.mixins import AuthorRequiredMixin


def event_detail(request, event_id):
    single_event = get_object_or_404(Event, pk=event_id)

    return render(request, 'event/event_detail.html', {'item': single_event})


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
                for i in range(int(delta)+1):
                    dates.add(start_date + timedelta(days=i))

    return render(request, 'event/calendar.html', {'events': dates})


def get_events(request):
    date = json.loads(request.GET.get('date'))
    date_ = datetime.strptime(f'{date["month"]}.{date["day"]}.{date["year"]}', '%m.%d.%Y').date()
    events = Event.objects.filter(is_published=True, date_start__lte=date_, date_end__gte=date_)
    stages = Stage.objects.filter(is_published=True, date_start__lte=date_, date_end__gte=date_)
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__lte=date_, date_end__gte=date_)
    result_list = sorted(list(chain(events, stages, tournaments)), key=attrgetter('date_start'))

    return render(request, 'event/events_by_date.html', {'events': result_list, 'date': date_, 'day_name': date['weekdayname']})


def get_weekly_events(request):
    date = json.loads(request.GET.get('date'))
    date_ = datetime.strptime(f'{date["month"]}.{date["day"]}.{date["year"]}', '%m.%d.%Y').date()
    week_start = date_ - timedelta(days=date['weekday'])
    week_end = week_start + timedelta(days=6)
    events = Event.objects.filter(is_published=True, date_start__range=[week_start, week_end])
    stages = Stage.objects.filter(is_published=True, date_start__range=[week_start, week_end])
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__range=[week_start, week_end])

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
        tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__range=[week_start, week_end])
        result_list = sorted(list(chain(events, stages, tournaments)), key=attrgetter('date_start'))

        events_dict[week] = dict(first=week_start, last=week_end, items=result_list)

    return render(request, 'event/events_by_month.html', {'events': events_dict})


def tournaments(request):
    tournaments_list = Tournament.objects.all()
    return render(request, 'event/tournaments.html', {'tournaments': tournaments_list})


def tournament_detail(request, tournament_id):
    single_tournament = get_object_or_404(Tournament, pk=tournament_id)
    stages = Stage.objects.filter(is_published=True, tournament=single_tournament.id)

    return render(request, 'event/tournament_detail.html', {'item': single_tournament, 'stages': stages})


def contest_detail(request, tournament_id):
    single_tournament = get_object_or_404(Tournament, pk=tournament_id)

    return render(request, 'event/tournament_detail.html', {'item': single_tournament})


def stage_detail(request, tournament_id, stage_id):
    single_stage = get_object_or_404(Stage, pk=stage_id)
    return render(request, 'event/stage-single.html', {'item': single_stage})


class EventCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Event
    template_name = 'event/event-create.html'
    form_class = EventCreateForm
    login_url = 'event_detail_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление события на сайт'
        return context

    def form_valid(self, form):
        # form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновление материала на сайте
    """
    model = Event
    template_name = 'event/event-update.html'
    context_object_name = 'item'
    form_class = EventUpdateForm
    login_url = 'main'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление записи: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class EventDeleteView(DeleteView):
    """
    Представление: удаления материала
    """
    model = Event
    success_url = reverse_lazy('calendar_page')
    context_object_name = 'post'
    template_name = 'event/event-delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context
