# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20150719_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='likes',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.ImageField(max_length=20, null=True, upload_to=b'photos/'),
            preserve_default=True,
        ),
    ]
