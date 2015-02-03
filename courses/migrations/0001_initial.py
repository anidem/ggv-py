# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('access_code', models.CharField(max_length=8, null=True, blank=True)),
            ],
            options={
                'permissions': (('view_course', 'Course Access'), ('edit_course', 'Instructor'), ('manage_course', 'Manager')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(related_name='crs_lessons', to='courses.Course')),
                ('lesson', models.ForeignKey(related_name='crs_courses', to='lessons.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
