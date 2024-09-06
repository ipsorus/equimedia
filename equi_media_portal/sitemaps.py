from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from articles.models import Article
from blog.models import BlogPost
from event.models import Tournament, Stage, Event
from news.models import NewsPost
from podcast.models import Video


class ArticleSitemap(Sitemap):
    """
    Карта-сайта для статей
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.time_update


class BlogSitemap(Sitemap):
    """
    Карта-сайта для блогов
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.time_update


class TournamentSitemap(Sitemap):
    """
    Карта-сайта для турниров
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Tournament.objects.all()

    def lastmod(self, obj):
        return obj.time_create


class StageSitemap(Sitemap):
    """
    Карта-сайта для этапов турниров
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Stage.objects.all()

    def lastmod(self, obj):
        return obj.time_create


class EventSitemap(Sitemap):
    """
    Карта-сайта для событий
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.time_create


class NewsPostSitemap(Sitemap):
    """
    Карта-сайта для новостей
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return NewsPost.objects.all()

    def lastmod(self, obj):
        return obj.time_update


class VideoSitemap(Sitemap):
    """
    Карта-сайта для подкастов
    """
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.time_update


class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц
    """

    def items(self):
        return ['feedback', 'main', 'articles_list_url', 'posts_list_url', 'calendar_page', 'tournaments',
                'news_list_url', 'video_list_url']

    def location(self, item):
        return reverse(item)
