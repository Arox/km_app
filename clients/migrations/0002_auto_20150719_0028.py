# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.FileField(max_length=10, null=True, upload_to=b'photos/'),
            preserve_default=True,
        ),
    ]
