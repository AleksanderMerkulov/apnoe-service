from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from medapp.views import main_page, upload_file, instruction, save_result

from medmed import settings

urlpatterns = [
    path('', main_page),
    path('form', upload_file),
    path('instruction', instruction),
    path('save_result/', save_result),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)