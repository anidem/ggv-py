# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(default=b'Message from ggvinteractive.com here.')),
                ('message_context', models.URLField(default=b'http://www.ggvinteractive.com', max_length=312)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='mark_type',
            field=models.CharField(default=b'none', max_length=32, choices=[(b'remember', b'Review,Revisa'), (b'todo', b'Need to Finish,Acabar'), (b'started', b'Start,Comienza'), (b'completed', b'Completed,Completado'), (b'question', b'Question,Pregunta'), (b'none', b'None,Borrar')]),
            preserve_default=True,
        ),
    ]
