# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_questionset_display_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='instructions',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
