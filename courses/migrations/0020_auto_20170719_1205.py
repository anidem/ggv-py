# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-19 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_course_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
