from django import forms

from news.models import NewsPost, Comment


class NewsPostCreateForm(forms.ModelForm):
    """
    Форма добавления новостей на сайте
    """

    class Meta:
        model = NewsPost
        fields = ('title', 'id', 'content', 'image', 'source_url', 'source_text', 'is_published')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False


class NewsPostUpdateForm(NewsPostCreateForm):
    """
    Форма обновления новости на сайте
    """

    class Meta:
        model = NewsPost
        fields = NewsPostCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False


class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к новостям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)