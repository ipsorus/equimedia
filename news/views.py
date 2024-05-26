from django.shortcuts import render, get_object_or_404

from news.models import NewsPost
from el_pagination.decorators import page_template


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@page_template('news/news-list-page.html')
def news_section(request,
                 template='news/news-list.html',
                 extra_context=None):
    context = {
        'news': NewsPost.objects.filter(is_published=True),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def news_detail(request, news_id):
    single_news = get_object_or_404(NewsPost, pk=news_id)
    news = NewsPost.objects.filter(is_published=True).exclude(pk=single_news.id)[:10]

    try:
        previous_post = single_news.get_previous_by_time_create()
    except NewsPost.DoesNotExist:
        previous_post = None

    try:
        next_post = single_news.get_next_by_time_create()
    except NewsPost.DoesNotExist:
        next_post = None

    data = {'title': single_news.title,
            'item': single_news,
            'news': news,
            'prev': previous_post,
            'next': next_post
            }

    return render(request, 'news/news-single.html', data)
