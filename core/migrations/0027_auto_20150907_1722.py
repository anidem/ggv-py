# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20150701_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemessage',
            name='url_context',
            field=models.CharField(default=b'http://www.ggvinteractive.com', max_length=512),
            preserve_default=True,
        ),
    ]
