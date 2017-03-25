# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-04 16:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_questionset_time_limit'),
        ('pretests', '0009_pretestusercompletion'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pretestusercompletion',
            unique_together=set([('pretestuser', 'completed_pretest')]),
        ),
    ]