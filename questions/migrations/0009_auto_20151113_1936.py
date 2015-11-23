# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_userworksheetscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userworksheetscore',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userworksheetscore',
            name='worksheet',
        ),
        migrations.DeleteModel(
            name='UserWorksheetScore',
        ),
        migrations.AddField(
            model_name='userworksheetstatus',
            name='score',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2),
            preserve_default=True,
        ),
    ]
