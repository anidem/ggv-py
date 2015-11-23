# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_section_subtitle'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('instructions', models.TextField(null=True, blank=True)),
                ('display_order', models.IntegerField()),
                ('activity_type', models.CharField(default=b'external_media', max_length=48, null=True)),
                ('media_link', models.URLField(help_text=b'copy and paste the link to the video. If you want to embed the video, please use the media embed field instead.', null=True, blank=True)),
                ('media_embed', models.TextField(help_text=b'copy and paste the embed code from video service (e.g. from YouTube)', null=True, blank=True)),
                ('lesson', models.ForeignKey(related_name='external_media', blank=True, to='lessons.Lesson', null=True)),
                ('section', models.ForeignKey(blank=True, to='lessons.Section', null=True)),
            ],
            options={
                'ordering': ['section', 'display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
