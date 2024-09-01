from podcast.models import VideoSettings


def video_settings(request):
    return {'video_settings': VideoSettings.load()}
