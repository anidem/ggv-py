# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20160210_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancetracker',
            name='day',
        ),
        migrations.AddField(
            model_name='attendancetracker',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 11, 6, 27, 41, 146760, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendancetracker',
            name='user',
            field=models.ForeignKey(related_name='attendance', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
