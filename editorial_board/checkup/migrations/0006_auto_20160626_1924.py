# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-26 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkup', '0005_auto_20160624_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='allow_save',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
