# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_auto_20160531_0151'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionresponse',
            unique_together=set([]),
        ),
    ]
