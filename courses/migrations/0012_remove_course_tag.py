# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-01 01:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20170131_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='tag',
        ),
    ]
