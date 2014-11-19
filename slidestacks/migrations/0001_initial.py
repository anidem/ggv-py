# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlideStack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('instructions', models.TextField(null=True)),
                ('display_order', models.IntegerField()),
                ('activity_type', models.CharField(default=b'slidestack', max_length=48, null=True)),
                ('asset', models.CharField(default=b'not specified', max_length=512, null=True, blank=True)),
                ('lesson', models.ForeignKey(related_name=b'slidestacks', blank=True, to='lessons.Lesson', null=True)),
                ('section', models.ForeignKey(blank=True, to='lessons.Section', null=True)),
            ],
            options={
                'ordering': ['section', 'display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
