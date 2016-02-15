# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20160210_2327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancetracker',
            old_name='date',
            new_name='datestamp',
        ),
    ]
