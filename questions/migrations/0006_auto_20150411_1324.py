# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20150406_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestion',
            name='display_key_file',
            field=models.FileField(null=True, upload_to=b'pdf', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_key_file',
            field=models.FileField(null=True, upload_to=b'pdf', blank=True),
            preserve_default=True,
        ),
    ]
