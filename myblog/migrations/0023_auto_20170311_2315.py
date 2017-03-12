# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0022_auto_20170311_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='ref',
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_title1',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_title2',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_title3',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_title4',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_title5',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_url1',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_url2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_url3',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_url4',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='todo',
            name='ref_url5',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Reference',
        ),
    ]