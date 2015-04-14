# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150402_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvuser',
            name='language_pref',
            field=models.CharField(default=b'english', max_length=32, choices=[(b'english', b'english'), (b'spanish', b'spanish')]),
            preserve_default=True,
        ),
    ]
