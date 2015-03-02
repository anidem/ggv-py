# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_userworksheetstatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userworksheetstatus',
            old_name='worksheet_completed',
            new_name='completed_worksheet',
        ),
    ]
