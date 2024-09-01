from django import forms

from testimonial.models import Testimonial


class TestimonialCreateForm(forms.ModelForm):
    """
    Форма добавления отзыва на сайте
    """

    class Meta:
        model = Testimonial
        fields = ('id', 'author', 'email', 'content')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['author'].widget.attrs.update({'class': 'form-control', "placeholder": 'ФИО автора'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', "placeholder": 'E-mail автора'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', "placeholder": 'Напишите что-нибудь о нас...'})
