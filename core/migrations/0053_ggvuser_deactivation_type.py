# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-28 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20171024_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvuser',
            name='deactivation_type',
            field=models.CharField(blank=True, choices=[(b'graduated', b'Graduated'), (b'relocated', b'Relocated'), (b'employed', b'Employed'), (b'inactivity', b'Inactivity')], max_length=48, null=True),
        ),
    ]