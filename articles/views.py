from django.shortcuts import render, get_object_or_404

from articles.models import Article
from el_pagination.decorators import page_template


@page_template('articles/articles-list-page.html')
def articles_section(request,
                     template='articles/articles-list.html',
                     extra_context=None):
    context = {
        'articles': Article.objects.filter(is_published=True),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def article_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    articles = Article.objects.filter(is_published=True).exclude(pk=article.id)[:10]

    data = {
        'item': article,
        'articles': articles
    }

    return render(request, 'articles/article-single.html', data)
