# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notetaker', '0004_auto_20170504_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='priority',
            field=models.IntegerField(blank=True, default=1000),
        ),
    ]
