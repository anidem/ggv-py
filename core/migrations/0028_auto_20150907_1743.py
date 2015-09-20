# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20150907_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemessage',
            name='url_context',
            field=models.CharField(default=b'/', unique=True, max_length=512),
            preserve_default=True,
        ),
    ]
