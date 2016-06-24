# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-22 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='freetext',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='choice',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='freetext',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='reporter',
            field=models.ForeignKey(blank=True, help_text=b'Reporter assigned to contact respondent for this survey.', null=True, on_delete=django.db.models.deletion.CASCADE, to='checkup.Reporter'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='display',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='ChoiceDisplay',
        ),
    ]
