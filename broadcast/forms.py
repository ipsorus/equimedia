from django import forms

from broadcast.models import Broadcast


class BroadcastCreateForm(forms.ModelForm):
    """
    Форма добавления трансляции на сайте
    """

    class Meta:
        model = Broadcast
        fields = ('title', 'id', 'broadcast_link', 'image', 'show_broadcast')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['show_broadcast'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['broadcast_link'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 5})


class BroadcastUpdateForm(BroadcastCreateForm):
    """
    Форма обновления трансляции на сайте
    """

    class Meta:
        model = Broadcast
        fields = BroadcastCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['show_broadcast'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['broadcast_link'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 5})
