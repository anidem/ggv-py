# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150402_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvuser',
            name='clean_logout',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
