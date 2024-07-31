from news.models import BannerNewsSideBar1, BannerNewsSideBar2, BannerNewsBetweenNews, NewsSettings


def news_advertisement_settings(request):
    return {'news_adv_settings': {1: BannerNewsSideBar1.load(),
                                  2: BannerNewsSideBar2.load(),
                                  3: BannerNewsBetweenNews.load(),
                                  }
            }


def news_settings(request):
    return {'news_settings': NewsSettings.load()}
