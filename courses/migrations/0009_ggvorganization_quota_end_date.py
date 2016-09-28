# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_ggvorganization_license_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvorganization',
            name='quota_end_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
