# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0018_auto_20170311_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('description', markdownx.models.MarkdownxField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('source', models.SlugField()),
                ('status', models.IntegerField(choices=[(1, '計画中'), (2, '進行中'), (3, '実装済')], default=1)),
                ('progress', models.IntegerField(choices=[(0, '0%'), (1, '10%'), (2, '20%'), (3, '30%'), (4, '40%'), (5, '50%'), (6, '60%'), (7, '70%'), (8, '80%'), (9, '90%'), (10, '100%')], default=1)),
            ],
        ),
    ]
