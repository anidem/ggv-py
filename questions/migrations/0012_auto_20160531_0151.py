# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_auto_20151122_1437'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='questionresponse',
            unique_together=set([('user', 'object_id', 'content_type')]),
        ),
    ]
