from .models import WebsiteSettings, SiteSettings


def website_settings(request):
    web_settings = WebsiteSettings.objects.filter(language=request.LANGUAGE_CODE).first()
    if not web_settings:
        web_settings = WebsiteSettings(language='fallback')
    return {'web_settings': web_settings}


def load_settings(request):
    return {'site_settings': SiteSettings.load()}
