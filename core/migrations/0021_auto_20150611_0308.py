# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150611_0229'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together=set([]),
        ),
    ]
