# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestion',
            name='sample_image',
            field=filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'PDF', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='sample_image',
            field=filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'PDF', blank=True),
            preserve_default=True,
        ),
    ]
