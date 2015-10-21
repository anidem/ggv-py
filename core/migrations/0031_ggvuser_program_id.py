# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20150921_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvuser',
            name='program_id',
            field=models.CharField(max_length=32, null=True),
            preserve_default=True,
        ),
    ]
