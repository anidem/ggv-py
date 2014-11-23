# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(related_name=b'crs_lessons', to='courses.Course')),
                ('lesson', models.ForeignKey(to='lessons.Lesson')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
