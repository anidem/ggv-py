# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20150629_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvuser',
            name='receive_email_messages',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ggvuser',
            name='receive_notify_email',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
