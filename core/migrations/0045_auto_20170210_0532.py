# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-10 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_ggvuser_last_deactivation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvuser',
            name='last_deactivation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
