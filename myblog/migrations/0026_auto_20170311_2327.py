# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0025_auto_20170311_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='ref_title1',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='ref_title2',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='ref_title3',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='ref_title4',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='ref_title5',
            field=models.CharField(default=' ', max_length=255),
        ),
    ]
