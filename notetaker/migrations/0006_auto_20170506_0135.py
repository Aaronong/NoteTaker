# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notetaker', '0005_auto_20170504_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='priority',
            field=models.IntegerField(default=1000),
        ),
    ]
