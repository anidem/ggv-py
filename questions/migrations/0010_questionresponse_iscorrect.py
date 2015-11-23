# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_auto_20151113_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionresponse',
            name='iscorrect',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
