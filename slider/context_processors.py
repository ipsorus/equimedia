from slider.models import SliderSettings


def slider_settings(request):
    return {'slider_settings': SliderSettings.load()}
