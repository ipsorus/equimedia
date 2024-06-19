from django import forms

from event.models import Event


class EventCreateForm(forms.ModelForm):
    """
    Форма добавления события на сайте
    """

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ["time_create"]
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
        self.fields['prize'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})


class EventUpdateForm(EventCreateForm):
    """
    Форма обновления события на сайте
    """

    class Meta:
        model = Event
        fields = EventCreateForm.Meta.fields
        exclude = ["time_create"]
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
        self.fields['prize'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['result'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
