# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 11:49
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0047_myservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myblog',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name=b'description'),
        ),
    ]
