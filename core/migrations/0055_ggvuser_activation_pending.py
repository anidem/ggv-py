# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-06 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_ggvuser_deactivation_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvuser',
            name='activation_pending',
            field=models.BooleanField(default=False),
        ),
    ]
