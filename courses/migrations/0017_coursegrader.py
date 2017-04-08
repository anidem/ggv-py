# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-07 12:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0016_auto_20170211_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGrader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_graders', to='courses.Course')),
                ('grader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_to_grade', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
