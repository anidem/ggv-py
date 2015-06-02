# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='mark_type',
            field=models.CharField(default=b'none', max_length=32, choices=[(b'remember', b'Review,Revisa'), (b'todo', b'Need to Finish,Acabar'), (b'started', b'Start,Comienza'), (b'completed', b'Completed,Completado'), (b'question', b'Question,Pregunta'), (b'none', b'None,Borrar')]),
            preserve_default=True,
        ),
    ]
