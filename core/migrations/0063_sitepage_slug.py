# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-02-11 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_auto_20180211_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepage',
            name='slug',
            field=models.SlugField(default='slugged', max_length=255),
            preserve_default=False,
        ),
    ]