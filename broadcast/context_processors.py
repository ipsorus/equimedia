from broadcast.models import BroadcastSettings


def broadcast_settings(request):
    return {'broadcast_settings': BroadcastSettings.load()}
