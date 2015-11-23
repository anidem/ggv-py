# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_questionresponse_iscorrect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userworksheetstatus',
            name='score',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
