# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supportmedia', '0002_auto_20151122_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalmedia',
            name='media_embed',
            field=models.TextField(help_text=b'copy and paste the embed code from video service (e.g. from YouTube)', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='externalmedia',
            name='media_link',
            field=models.URLField(help_text=b'copy and paste the link to the video. If you want to embed the video, please use the media embed field instead.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
