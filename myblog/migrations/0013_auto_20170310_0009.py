# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0012_auto_20170306_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myblog',
            name='body',
            field=models.CharField(max_length=20000),
        ),
    ]
