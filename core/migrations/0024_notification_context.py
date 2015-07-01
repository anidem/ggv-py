# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20150627_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='context',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
