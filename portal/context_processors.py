from .models import SiteSettings, ContactsSettings, AboutUsSettings, SocialsSettings


def load_settings(request):
    return {'site_settings': SiteSettings.load()}


def contacts_settings(request):
    return {'contacts_settings': ContactsSettings.load()}


def about_us_settings(request):
    return {'about_us_settings': AboutUsSettings.load()}


def socials_settings(request):
    return {'social_settings': SocialsSettings.load()}
