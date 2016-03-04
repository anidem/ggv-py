# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20160213_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetracker',
            name='code',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Online'), (1, b'Pre Testing'), (2, b'Testing'), (3, b'Excused'), (4, b'In Class')]),
            preserve_default=True,
        ),
    ]
