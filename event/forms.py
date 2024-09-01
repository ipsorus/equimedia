from django import forms

from event.models import Event, EventDocument, TournamentDocument, Tournament, Stage, StageDocument, \
    TournamentCloseDocument, StageCloseDocument


class EventCreateForm(forms.ModelForm):
    """
    Форма добавления события на сайте
    """

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ["time_create", "author"]
        widgets = {
            'date_start': forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_end': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['event_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})


class EventDocumentCreateForm(forms.ModelForm):
    """
    Форма добавления документов для события на сайте
    """

    class Meta:
        model = EventDocument
        fields = '__all__'
        exclude = ["time_create"]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class EventUpdateForm(EventCreateForm):
    """
    Форма обновления события на сайте
    """

    class Meta:
        model = Event
        fields = EventCreateForm.Meta.fields
        exclude = ["time_create", "author"]
        widgets = {
            'date_start': forms.widgets.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'date_end': forms.widgets.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['event_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})


class TournamentCreateForm(forms.ModelForm):
    """
    Форма добавления турнира на сайте
    """

    class Meta:
        model = Tournament
        fields = '__all__'
        exclude = ["time_create", "author"]
        widgets = {
            'date_start': forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_end': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['discipline'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['prize'].widget.attrs.update({'class': 'form-control'})


class TournamentUpdateForm(TournamentCreateForm):
    """
    Форма обновления турнира на сайте
    """

    class Meta:
        model = Tournament
        fields = TournamentCreateForm.Meta.fields
        exclude = ["time_create", "author"]
        widgets = {
            'date_start': forms.widgets.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'date_end': forms.widgets.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_closed'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['discipline'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['prize'].widget.attrs.update({'class': 'form-control'})


class TournamentDocumentCreateForm(forms.ModelForm):
    """
    Форма добавления документов для турнира на сайте
    """

    class Meta:
        model = TournamentDocument
        fields = '__all__'
        exclude = ["time_create"]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class TournamentDocumentCloseForm(forms.ModelForm):
    """
    Форма добавления документов для турнира на сайте
    """

    class Meta:
        model = TournamentCloseDocument
        fields = '__all__'
        exclude = ["time_create"]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class TournamentStageCreateForm(forms.ModelForm):
    """
    Форма добавления этапов для турнира на сайте
    """

    class Meta:
        model = Stage
        fields = '__all__'
        exclude = ["time_create", "author", "stage_type"]
        widgets = {
            'date_start': forms.widgets.DateInput(attrs={'type': 'date'}),
            'date_end': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_closed'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['discipline'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['prize'].widget.attrs.update({'class': 'form-control'})


class StageUpdateForm(TournamentStageCreateForm):
    """
    Форма обновления турнира на сайте
    """

    class Meta:
        model = Stage
        fields = TournamentStageCreateForm.Meta.fields
        exclude = ["time_create", "author", "stage_type"]
        widgets = {
            'date_start': forms.widgets.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'date_end': forms.widgets.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_closed'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['discipline'].widget.attrs.update({'class': 'form-select'})
        self.fields['tournament'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['prize'].widget.attrs.update({'class': 'form-control'})


class StageDocumentCreateForm(forms.ModelForm):
    """
    Форма добавления документов для турнира на сайте
    """

    class Meta:
        model = StageDocument
        fields = '__all__'
        exclude = ["time_create"]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class StageDocumentCloseForm(forms.ModelForm):
    """
    Форма добавления документов для этапа турнира на сайте
    """

    class Meta:
        model = StageCloseDocument
        fields = '__all__'
        exclude = ["time_create"]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})


class TournamentCloseForm(forms.ModelForm):
    """
    Форма закрытия турнира на сайте
    """

    class Meta:
        model = Tournament
        fields = ["result", "is_closed"]
        exclude = ['date_start', 'date_end', "time_create", "author", 'discipline', 'type', 'description', 'location', 'prize']

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_closed'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})


class StageCloseForm(forms.ModelForm):
    """
    Форма добавления документов для этапа турнира на сайте
    """

    class Meta:
        model = Stage
        fields = ["result", "is_closed"]
        exclude = ['date_start', 'date_end', "time_create", "author", 'discipline', 'type', 'description', 'location',
                   'prize']

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
