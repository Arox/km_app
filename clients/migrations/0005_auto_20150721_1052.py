# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import third_party.image_field
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20150720_2149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'client', 'verbose_name_plural': 'clients'},
        ),
        migrations.AlterField(
            model_name='client',
            name='birthday',
            field=models.DateField(help_text='format: d.m.yyyy', verbose_name='birthday'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='likes', validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=40, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=third_party.image_field.ResizedImageField(max_length=20, null=True, upload_to=b'photos/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='sername',
            field=models.CharField(max_length=60, verbose_name='sername'),
            preserve_default=True,
        ),
    ]
