# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20150318_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestion',
            name='response_required',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='response_required',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
