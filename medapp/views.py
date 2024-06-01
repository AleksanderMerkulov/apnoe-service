import io

from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, TableStyle, Table

from .forms import UploadForm
import os

from medmed import settings


# Create your views here.

def main_page(request):
    return render(request, 'index.html')


def instruction(request):
    return render(request, 'instruction.html')

def checkFile(filepath):
    print(filepath)



def file_handler(file):
    UPLOAD_DIRECTORY = settings.MEDIA_ROOT
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    filepath = os.path.join(UPLOAD_DIRECTORY, file.name)

    with open(filepath, 'wb+') as d:
        for ch in file.chunks():
            d.write(ch)

    # здесь должна быть функция, которой я передам управление файлом,
    # допустим для его чтения - отдаём filepath.

    pass


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_handler(request.FILES['file'])


            apnoe = None
            apnoe_type = None
            context = {
                'apnoe': apnoe,
                'apnoe_type': apnoe_type,
                'filename': request.FILES['file'].name
            }

            return render(request, 'result.html', context)
            # return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/err_load_file')
    else:
        form = UploadForm()
        return render(request, 'form.html', {'form':form})


def save_result(request):

    # получаем параметры из запроса на сохранение файла
    params = request.GET.items()

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    # Настройка PDF
    pdf_filename = "result.pdf"
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Определение стилей
    styles = getSampleStyleSheet()
    styleH = styles["Heading1"]

    # Форматирование данных в виде списка списков для таблицы
    table_header = []
    # table_header = ['Апное', "Тип апное", "Название файла"]
    table_body = []
    for param in params:
        table_header.append(param[0])
        table_body.append(param[1])
    table_data = [table_header, table_body]  # заголовки таблицы

    # Создание таблицы с данными
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ]))

    # Добавление таблицы в элементы PDF
    elements.append(table)

    # Генерация PDF
    doc.build(elements)

    # Сброс указателя потока обратно в начало
    buffer.seek(0)

    # Создание FileResponse
    response = FileResponse(buffer, as_attachment=True, filename=pdf_filename)

    return response