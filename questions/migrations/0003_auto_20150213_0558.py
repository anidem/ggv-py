# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20150213_0509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optionquestion',
            name='sample_image',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='sample_image',
        ),
    ]
