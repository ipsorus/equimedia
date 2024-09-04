from django import forms
from slider.models import Slider


class SliderCreateForm(forms.ModelForm):
    """
    Форма добавления слайда на сайте
    """

    class Meta:
        model = Slider
        fields = ('title', 'additional_content', 'poster', 'video', 'is_video', 'is_published', 'third_party_site', 'url')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 2})
        self.fields['additional_content'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['is_video'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['third_party_site'].widget.attrs.update({'class': 'form-check-input'})


class SliderUpdateForm(SliderCreateForm):
    """
    Форма обновления слайдера на сайте
    """

    class Meta:
        model = Slider
        fields = SliderCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 2})
        self.fields['additional_content'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['is_video'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['third_party_site'].widget.attrs.update({'class': 'form-check-input'})
