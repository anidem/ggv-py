# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20150411_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='userworksheetstatus',
            name='can_check_results',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
