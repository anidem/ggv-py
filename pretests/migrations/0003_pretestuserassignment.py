# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-20 03:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_20170218_1026'),
        ('pretests', '0002_auto_20170218_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='PretestUserAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pretest_lessons', to='lessons.Lesson')),
                ('pretestuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pretest_assignments', to='pretests.PretestUser')),
            ],
        ),
    ]
