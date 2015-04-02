# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150401_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggvuser',
            name='clean_logout',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='mark_type',
            field=models.CharField(default=b'marked', max_length=32, choices=[(b'remember', b'Remember'), (b'todo', b'To do'), (b'started', b'Started'), (b'completed', b'Completed'), (b'question', b'Question'), (b'none', b'None')]),
            preserve_default=True,
        ),
    ]
