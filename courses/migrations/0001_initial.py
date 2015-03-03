# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0001_initial'),
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
                'permissions': (('access', 'Access'), ('instructor', 'Instructor'), ('manage', 'Manager')),
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
        migrations.CreateModel(
            name='CoursePermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'student', max_length=48, choices=[(b'manager', b'Manager'), (b'instructor', b'Instructor'), (b'student', b'Student')])),
                ('course', models.ForeignKey(related_name='course_permissions', to='courses.Course')),
                ('user', models.ForeignKey(related_name='user_course_permissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
