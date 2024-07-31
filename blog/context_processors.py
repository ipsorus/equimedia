from blog.models import BlogSettings, BannerBlogSidebar, BannerBlogSidebar2


def blog_advertisement_settings(request):
    return {'blog_adv_settings': {
                             1: BannerBlogSidebar.load(),
                             2: BannerBlogSidebar2.load()
                             }
            }


def blog_settings(request):
    return {'blog_settings': BlogSettings.load()}
