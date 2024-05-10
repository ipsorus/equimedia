from django.shortcuts import render, get_object_or_404

from articles.models import Article


def article_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    articles = Article.objects.filter(is_published=True).exclude(pk=article.id)[:10]

    data = {'title': article.title,
            'item': article,
            'articles': articles
            }

    return render(request, 'articles/article-single.html', data)
