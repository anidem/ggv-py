# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Subject', max_length=256)),
                ('subject', models.CharField(max_length=32, choices=[(b'math', b'math'), (b'science', b'science'), (b'socialstudies', b'socialstudies'), (b'writing', b'writing'), (b'default', b'default')])),
                ('language', models.CharField(default=b'eng', max_length=32, choices=[(b'eng', b'English'), (b'span', b'Spanish')])),
                ('icon_class', models.CharField(default=b'university', max_length=32, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('display_order', models.IntegerField(default=0)),
                ('lesson', models.ForeignKey(related_name=b'sections', to='lessons.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'display_order', 'title'],
            },
            bases=(models.Model,),
        ),
    ]
