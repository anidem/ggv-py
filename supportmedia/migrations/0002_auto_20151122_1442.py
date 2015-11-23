# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supportmedia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalmedia',
            name='media_link',
            field=models.URLField(default=b'http://www.google.com'),
            preserve_default=True,
        ),
    ]
