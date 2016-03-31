# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20160320_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvorganization',
            name='license_id',
            field=models.CharField(max_length=48, null=True),
            preserve_default=True,
        ),
    ]
