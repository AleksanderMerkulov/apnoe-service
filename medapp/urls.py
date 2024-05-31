from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from medapp.views import main_page, upload_file

from medmed import settings

urlpatterns = [
    path('', main_page),
    path('form', upload_file)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)