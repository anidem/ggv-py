# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestion',
            name='display_pdf',
            field=models.FileField(null=True, upload_to=b'pdf', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_pdf',
            field=models.FileField(null=True, upload_to=b'pdf', blank=True),
            preserve_default=True,
        ),
    ]
