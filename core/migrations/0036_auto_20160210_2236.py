# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_attendancetracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancetracker',
            name='code',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Online'), (1, b'In Class'), (2, b'Excused')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attendancetracker',
            name='day',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
