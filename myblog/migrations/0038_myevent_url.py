# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0037_myreference_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='myevent',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
