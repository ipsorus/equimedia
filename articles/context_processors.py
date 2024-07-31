from articles.models import ArticlesSettings, BannerArticleBetweenArticles, BannerArticleSideBar2, BannerArticleSideBar1


def article_advertisement_settings(request):
    return {'article_adv_settings': {
                             1: BannerArticleSideBar1.load(),
                             2: BannerArticleSideBar2.load(),
                             3: BannerArticleBetweenArticles.load(),
                             }
            }


def articles_settings(request):
    return {'articles_settings': ArticlesSettings.load()}
