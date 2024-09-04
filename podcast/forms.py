from django import forms

from podcast.models import Video


class VideoCreateForm(forms.ModelForm):
    """
    Форма добавления видео на сайте
    """

    class Meta:
        model = Video
        fields = ('title', 'id', 'image', 'video_link', 'short', 'is_published')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['short'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['video_link'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['short'].required = False


class VideoUpdateForm(VideoCreateForm):
    """
    Форма обновления видео на сайте
    """

    class Meta:
        model = Video
        fields = VideoCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['video_link'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['short'].widget.attrs.update({'class': 'form-control', 'cols': 20, 'rows': 3})
        self.fields['short'].required = False
