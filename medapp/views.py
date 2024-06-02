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
import numpy as np

from medmed import settings
from .net import Network


# Create your views here.

def main_page(request):
    return render(request, 'tizer.html')


def instruction(request):
    return render(request, 'instruction.html')


def getApnoeIndex(results, path):
    import scipy

    y = np.array(results)
    b, a = scipy.signal.butter(3, 0.9, 'low')
    out = scipy.signal.filtfilt(b, a, y)
    freq = 0
    with open(path) as f1:
        for line in f1.readlines():
            splat = line.split(':')
            if splat[0] == '"SampleFrequency':
                freq = int(splat[1].split('Hz')[0])
                break
    return len(scipy.signal.find_peaks(out)[0]) * freq / len(y)


def fileToASCII(filename, channel):
    file_with_dot = f'{filename}.REC'
    pth = f'./media/{filename}'
    pth_with_dot = f'./media/{file_with_dot}'

    print(os.path.abspath(pth))
    os.system(f'.\Programs\EDFtoASCII\EDFToASCII.exe "{pth_with_dot}" {channel} "{pth}.txt" "{pth}.ascii" /BATCH')
    # os.system(f'.\Programs\EDFtoASCII\EDFToASCII.exe "{file_with_dot}" {channel} "{pth}.txt" "{pth}.ascii" /BATCH')
    # print(f'{os.path.exists()}')
    res = []
    with open(f'{pth}.ascii') as f:
        for line in f.readlines():
            res.append(float(line.strip()))

    # get an apnoe index for later use
    index = getApnoeIndex(res, f'{pth}.txt')

    os.remove(f'{pth}.txt')
    os.remove(f'{pth}.ascii')
    return [res, index]


def do_result(request):
    size = 10  # не знаю почему он есть
    n1 = Network(size)
    n2 = Network(size)
    try:
        n1.loadWeights('./Progozavry/1.weights.h5')
        n2.loadWeights('./Progozavry/2.weights.h5')
    except:
        HttpResponseRedirect('/err_of_work')
        pass

    pass
    data1 = []
    # Process the first segment
    tr = fileToASCII(request.FILES['file'].name.split('.')[0], 3)  # get a test-set-sample
    apnoe_index1 = tr[1]  # get an apnoe_index from getApnoeIndex
    tr = tr[0]  # reform tr to tr correct GAVNOKOD - do refactor this one

    tr2 = []
    rate = len(tr) // (512 * 512)
    for i in range(0, len(tr), rate):
        p = 0.0
        if i + rate >= len(tr):
            rate = len(tr) - i
        for j in range(rate):
            p += tr[i + j]
        tr2.append(p / rate)
        if len(tr2) == 512 * 512:
            break
    data1.append(tr2)
    data1 = np.array(data1).reshape((-1, 512, 512, 1))


    data2 = []
    # Process the first segment
    tr = fileToASCII(request.FILES['file'].name.split('.')[0], 6)  # get a test-set-sample
    apnoe_index2 = tr[1]  # get an apnoe_index from getApnoeIndex
    tr = tr[0]  # reform tr to correct tr GAVNOKOD - do refactor this one
    tr2 = []
    rate = len(tr) // (512 * 512)
    for i in range(0, len(tr), rate):
        p = 0.0
        if i + rate >= len(tr):
            rate = len(tr) - i
        for j in range(rate):
            p += tr[i + j]
        tr2.append(p / rate)
        if len(tr2) == 512 * 512:
            break
    data2.append(tr2)
    data2 = np.array(data2).reshape((-1, 512, 512, 1))
    net1_response = n1.predict(data1)
    net2_response = n2.predict(data2)
    return [net1_response, net2_response, [apnoe_index1, apnoe_index2]]


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
            file_handler(request.FILES['file'])  # upload file to server
            # test_sample = fileToASCII(request.FILES['file'].name.split('.')[0], 3)  # get a test-set-sample

            result = do_result(request)
            # result = [[1, 0][1, 0]]

            # print(result)
            # Получение результатов.
            apnoe = ((result[0][1] + result[1][1]) / 2)  # veroiatnost chto eto apnoe
            apnoe_index = ((result[2][1] + result[2][1]) / 2)
            apnoe_type = ''
            if 15 > apnoe_index >= 5:
                apnoe_type = 'Легкая'
            elif 30 > apnoe_index >= 15:
                apnoe_type = 'Средняя'
            elif apnoe_index >= 30:
                apnoe_type = 'Тяжёлая'

            apnoe_detect = ''
            if apnoe <= 5:
                apnoe_detect = "Отсутствует"
                apnoe_type = '-'
            elif 95 > apnoe > 5:
                apnoe_detect = 'Возможно присутствует'
            elif apnoe >= 95:
                apnoe_detect = 'Обнаружено'


            # Передача результатов для рендера на странице.
            context = {
                'apnoe': apnoe,
                'apnoe_type': apnoe_type,
                'filename': request.FILES['file'].name,
                'apnoe_detect': apnoe_detect
            }

            return render(request, 'result.html', context)
            # return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/err_load_file')
    else:
        form = UploadForm()
        return render(request, 'form.html', {'form': form})


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
