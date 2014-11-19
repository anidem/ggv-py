# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20141107_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'ordering': ['display_order', 'id']},
        ),
        migrations.AlterModelOptions(
            name='questionsequenceitem',
            options={},
        ),
        migrations.RemoveField(
            model_name='questionsequenceitem',
            name='order',
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'img', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'img', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='questionsequenceitem',
            name='question_sequence',
            field=models.ForeignKey(related_name=b'sequence_items', to='questions.QuestionSet'),
        ),
        migrations.AlterField(
            model_name='textquestion',
            name='input_size',
            field=models.CharField(default=b'1', max_length=64, choices=[(b'1', b'short answer: (1 row 50 cols)'), (b'5', b'sentence: (5 rows 50 cols'), (b'15', b'paragraph(s): (15 rows 50 cols)')]),
        ),
    ]
