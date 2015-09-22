# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_sitepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ggvuser',
            name='receive_email_messages',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ggvuser',
            name='receive_notify_email',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
