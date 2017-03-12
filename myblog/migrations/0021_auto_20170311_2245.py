# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0020_auto_20170311_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='progress',
            field=models.IntegerField(choices=[(0, '0%'), (1, '10%'), (2, '20%'), (3, '30%'), (4, '40%'), (5, '50%'), (6, '60%'), (7, '70%'), (8, '80%'), (9, '90%'), (10, '100%')], default=0),
        ),
    ]