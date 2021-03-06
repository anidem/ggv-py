# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-18 17:20
from __future__ import unicode_literals

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pretests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pretestuser',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='pretestuser',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
