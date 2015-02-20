# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20150220_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionsequenceitem',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='questionsequenceitem',
            name='question_sequence',
        ),
        migrations.DeleteModel(
            name='QuestionSequenceItem',
        ),
    ]
