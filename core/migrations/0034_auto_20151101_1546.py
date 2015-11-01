# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20151018_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvuser',
            name='program_id',
            field=models.CharField(max_length=32, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
