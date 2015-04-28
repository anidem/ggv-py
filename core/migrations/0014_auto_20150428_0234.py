# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_activitylog_message_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='user',
            field=models.ForeignKey(related_name='activitylog', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='mark_type',
            field=models.CharField(default=b'none', max_length=32, choices=[(b'remember', b'Review'), (b'todo', b'Need to Finish'), (b'started', b'Start'), (b'completed', b'Completed'), (b'question', b'Question'), (b'none', b'None')]),
            preserve_default=True,
        ),
    ]
