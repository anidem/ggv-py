# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-07 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0015_textquestion_auto_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionresponse',
            name='grade_request_sent',
            field=models.BooleanField(default=False),
        ),
    ]