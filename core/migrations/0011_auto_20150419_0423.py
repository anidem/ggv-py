# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150419_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='action',
            field=models.CharField(max_length=32, choices=[(b'login', b'login'), (b'logout', b'logout'), (b'access-question-text', b'access text question'), (b'access-question-option', b'access multiple choice'), (b'access-presentation', b'access presentation'), (b'access-worksheet', b'access worksheet')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='message',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
    ]
