# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-18 04:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pretests', '0013_auto_20170305_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='pretestusercompletion',
            name='confirm_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pretestaccount',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pretest_user_account', to=settings.AUTH_USER_MODEL),
        ),
    ]
