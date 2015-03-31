# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150329_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='action',
            field=models.CharField(max_length=32, choices=[(b'login', b'login'), (b'logout', b'logout'), (b'access-question-text', b'access text question'), (b'access-question-option', b'access multiple choice'), (b'access-presentation', b'access presentation')]),
            preserve_default=True,
        ),
    ]
