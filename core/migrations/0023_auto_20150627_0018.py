# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20150611_1356'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together=set([('mark_type', 'creator', 'content_type', 'object_id', 'course_context')]),
        ),
    ]
