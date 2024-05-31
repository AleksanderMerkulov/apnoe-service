from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadForm
import os

from medmed import settings


# Create your views here.

def main_page(request):
    return render(request, 'index.html')


def file_handler(file):
    UPLOAD_DIRECTORY = settings.MEDIA_ROOT
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    filepath = os.path.join(UPLOAD_DIRECTORY, file.name)

    with open(filepath, 'wb+') as d:
        for ch in file.chunks():
            d.write(ch)
    pass


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        file_handler(request.FILES['file'])
        return HttpResponseRedirect('/')
    else:
        form = UploadForm()
        return render(request, 'form.html', {'form':form})