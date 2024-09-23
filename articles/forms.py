from django import forms

from articles.models import Article, Comment


class ArticlePostCreateForm(forms.ModelForm):
    """
    Форма добавления статьи на сайте
    """

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['slider'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False


class ArticlePostUpdateForm(ArticlePostCreateForm):
    """
    Форма обновления статьи на сайте
    """

    class Meta:
        model = Article
        fields = ArticlePostCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['slider'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False


class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к статьям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)