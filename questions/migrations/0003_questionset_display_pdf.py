# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20150318_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='display_pdf',
            field=models.FileField(null=True, upload_to=b'pdf', blank=True),
            preserve_default=True,
        ),
    ]
