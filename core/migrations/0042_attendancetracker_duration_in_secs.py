# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20160320_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancetracker',
            name='duration_in_secs',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
