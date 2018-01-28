# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-01-28 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_auto_20180128_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvaccountrequest',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_requests', to='courses.Course'),
        ),
    ]
