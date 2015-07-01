# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_notification_context'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='logdata',
            field=models.ForeignKey(blank=True, to='core.ActivityLog', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='event',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
    ]
