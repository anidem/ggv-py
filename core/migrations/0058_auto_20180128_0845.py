# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-28 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_ggvaccountrequest_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvaccountrequest',
            name='note',
            field=models.TextField(null=True),
        ),
    ]