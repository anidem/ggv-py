# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150331_2314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitylog',
            options={'ordering': ['user', '-timestamp']},
        ),
    ]
