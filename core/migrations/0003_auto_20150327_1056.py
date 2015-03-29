# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_validationlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validationlist',
            name='user',
        ),
        migrations.AddField(
            model_name='validationlist',
            name='user_email',
            field=models.CharField(default='admin@ruby.mcl', max_length=128),
            preserve_default=False,
        ),
    ]
