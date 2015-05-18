# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150517_2335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitemessage',
            old_name='message_context',
            new_name='url_context',
        ),
        migrations.AddField(
            model_name='sitemessage',
            name='show',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
