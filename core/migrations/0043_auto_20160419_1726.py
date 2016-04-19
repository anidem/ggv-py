# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_attendancetracker_duration_in_secs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetracker',
            name='code',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Online'), (1, b'Pretest'), (2, b'Official Test'), (3, b'Graduated'), (4, b'Dropped'), (5, b'Limited Activity')]),
            preserve_default=True,
        ),
    ]
