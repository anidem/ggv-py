# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150414_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='mark_type',
            field=models.CharField(default=b'marked', max_length=32, choices=[(b'remember', b'Review'), (b'todo', b'Need to Finish'), (b'started', b'Start'), (b'completed', b'Completed'), (b'question', b'Question'), (b'none', b'None')]),
            preserve_default=True,
        ),
    ]
