# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0043_auto_20170313_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.IntegerField(choices=[(1, b'\xe8\xa8\x88\xe7\x94\xbb\xe4\xb8\xad'), (2, b'\xe9\x80\xb2\xe8\xa1\x8c\xe4\xb8\xad'), (3, b'\xe5\xae\x9f\xe8\xa3\x85\xe6\xb8\x88')], default=1),
        ),
    ]
