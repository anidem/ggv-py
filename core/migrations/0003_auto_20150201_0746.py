# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_activitylog_target'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitylog',
            name='target',
        ),
        migrations.AddField(
            model_name='activitylog',
            name='message',
            field=models.CharField(default='none', max_length=64),
            preserve_default=False,
        ),
    ]
