# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20160303_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetracker',
            name='code',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Online'), (1, b'Pretest'), (2, b'Official Test'), (3, b'Graduated'), (4, b'Dropped')]),
            preserve_default=True,
        ),
    ]
