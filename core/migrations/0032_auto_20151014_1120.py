# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_ggvuser_program_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvuser',
            name='program_id',
            field=models.CharField(default=b'', max_length=32, null=True),
            preserve_default=True,
        ),
    ]
