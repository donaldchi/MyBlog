# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0027_auto_20170311_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='source_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
