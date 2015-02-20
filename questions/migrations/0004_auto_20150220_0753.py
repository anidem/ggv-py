# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20150213_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestion',
            name='question_set',
            field=models.ForeignKey(related_name='option_questions', default=0, to='questions.QuestionSet'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='question_set',
            field=models.ForeignKey(related_name='text_questions', default=0, to='questions.QuestionSet'),
            preserve_default=False,
        ),
    ]
