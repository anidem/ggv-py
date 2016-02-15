# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20160213_0833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendancetracker',
            options={'ordering': ['user', 'datestamp']},
        ),
        migrations.AddField(
            model_name='attendancetracker',
            name='datestr',
            field=models.CharField(default=b'', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attendancetracker',
            unique_together=set([('user', 'datestr')]),
        ),
    ]
