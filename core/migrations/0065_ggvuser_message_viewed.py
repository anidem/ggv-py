# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-03-10 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_auto_20180310_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvuser',
            name='message_viewed',
            field=models.BooleanField(default=True),
        ),
    ]