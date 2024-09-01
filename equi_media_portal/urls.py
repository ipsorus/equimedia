from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from equi_media_portal import settings
from django.views.static import serve as mediaserve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('', include('articles.urls')),
    path('', include('news.urls')),
    path('', include('event.urls')),
    path('', include('blog.urls')),
    path('', include('account.urls')),
    path('', include('podcast.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]

handler403 = 'portal.views.tr_handler403'
handler404 = 'portal.views.tr_handler404'
handler500 = 'portal.views.tr_handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += [
        path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
             mediaserve, {'document_root': settings.MEDIA_ROOT}),
        path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
             mediaserve, {'document_root': settings.STATIC_ROOT}),
    ]
