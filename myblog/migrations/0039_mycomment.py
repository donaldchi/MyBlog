# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 07:06
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0038_myevent_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('body', markdownx.models.MarkdownxField()),
                ('publishing_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]