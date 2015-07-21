# -*- coding: utf-8 -*-
import xlsxwriter
from km_app.celery import app
from models import Client
import km_app.settings
import os

@app.task
def report():
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('./static/docs/report.xlsx')

    start_row = 4
    start_column = 4

    for client in Client.objects.all():
        worksheet = workbook.add_worksheet()
        worksheet.write(start_row, start_column, u'Имя')
        worksheet.write(start_row + 1, start_column, u'Фамилия')
        worksheet.write(start_row + 2, start_column, u'Дата рождения')
        worksheet.write(start_row + 3, start_column, u'Возраст')

        worksheet.write(start_row, start_column + 1, client.name)
        worksheet.write(start_row + 1, start_column + 1, client.sername)
        worksheet.write(start_row + 2, start_column + 1, client.birthday.strftime('%d.%m.%Y'))
        worksheet.write(start_row + 3, start_column + 1, client.age)

        if client.photo is not None and len(client.photo.name) > 0:
            # Insert an image.
            worksheet.insert_image(1, 0, os.path.realpath(os.path.join(km_app.settings.MEDIA_ROOT, client.photo.name)))

    workbook.close()