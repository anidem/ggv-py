# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='subtitle',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
