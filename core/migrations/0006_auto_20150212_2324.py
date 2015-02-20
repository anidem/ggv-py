# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='mark_type',
            field=models.CharField(default=b'marked', max_length=32, choices=[(b'remember', b'Remember'), (b'todo', b'Todo'), (b'started', b'Started'), (b'completed', b'Completed'), (b'question', b'Question'), (b'none', b'None')]),
            preserve_default=True,
        ),
    ]
