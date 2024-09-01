from event.models import BannerEventSideBar1, BannerEventSideBar2, EventSettings


def event_advertisement_settings(request):
    return {'event_adv_settings': {
                             1: BannerEventSideBar1.load(),
                             2: BannerEventSideBar2.load()
                             }
            }


def event_settings(request):
    return {'event_settings': EventSettings.load()}
