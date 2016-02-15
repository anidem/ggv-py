# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0034_auto_20151101_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceTracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField(auto_now_add=True)),
                ('code', models.PositiveIntegerField(default=0, choices=[(b'remember', b'Review,Revisa'), (b'todo', b'Need to Finish,Acabar'), (b'started', b'Start,Comienza'), (b'completed', b'Completed,Completado'), (b'question', b'Question,Pregunta'), (b'none', b'None,Borrar')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
