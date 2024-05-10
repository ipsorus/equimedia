from django.contrib import admin
from django.urls import path, include

from portal import views
from portal.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('', include('articles.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]

handler404 = page_not_found
