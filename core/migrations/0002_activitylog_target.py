# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='target',
            field=models.CharField(default='worksheet', max_length=32),
            preserve_default=False,
        ),
    ]
