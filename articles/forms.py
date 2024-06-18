from django import forms

from articles.models import Article


class ArticlePostCreateForm(forms.ModelForm):
    """
    Форма добавления статьи на сайте
    """

    class Meta:
        model = Article
        fields = ('title', 'id', 'content', 'image', 'is_published')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
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

        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False
