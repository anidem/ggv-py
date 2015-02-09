# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('courses', '0001_initial'),
        ('core', '0004_auto_20150201_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mark_type', models.CharField(default=b'marked', max_length=32, choices=[(b'marked', b'Marker'), (b'todo', b'Todo'), (b'started', b'Started'), (b'completed', b'Completed'), (b'question', b'Question')])),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name='bookmarks', to='contenttypes.ContentType')),
                ('course_context', models.ForeignKey(blank=True, to='courses.Course', null=True)),
                ('creator', models.ForeignKey(related_name='bookmarker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
