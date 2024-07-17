from advertisements.models import BannerNewsSideBar1, BannerNewsSideBar2, BannerNewsBetweenNews, BannerArticleSideBar1, \
    BannerArticleSideBar2, BannerArticleBetweenArticles, BannerBlogSidebar, BannerBlogSidebar2
from .models import WebsiteSettings, SiteSettings, ContactsSettings, AboutUsSettings, SocialsSettings, NewsSettings, \
    ArticlesSettings, SliderSettings, BlogSettings


# def website_settings(request):
#     web_settings = WebsiteSettings.objects.filter(language=request.LANGUAGE_CODE).first()
#     if not web_settings:
#         web_settings = WebsiteSettings(language='fallback')
#     return {'web_settings': web_settings}


def load_settings(request):
    return {'site_settings': SiteSettings.load()}


def advertisement_settings(request):
    return {'adv_settings': {1: BannerNewsSideBar1.load(),
                             2: BannerNewsSideBar2.load(),
                             3: BannerNewsBetweenNews.load(),
                             4: BannerArticleSideBar1.load(),
                             5: BannerArticleSideBar2.load(),
                             6: BannerArticleBetweenArticles.load(),
                             7: BannerBlogSidebar.load(),
                             8: BannerBlogSidebar2.load()
                             }
            }


def contacts_settings(request):
    return {'contacts_settings': ContactsSettings.load()}


def about_us_settings(request):
    return {'about_us_settings': AboutUsSettings.load()}


def socials_settings(request):
    return {'social_settings': SocialsSettings.load()}


def news_settings(request):
    return {'news_settings': NewsSettings.load()}


def articles_settings(request):
    return {'articles_settings': ArticlesSettings.load()}


def slider_settings(request):
    return {'slider_settings': SliderSettings.load()}


def blog_settings(request):
    return {'blog_settings': BlogSettings.load()}
