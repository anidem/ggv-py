# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20160320_1948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['ggv_organization__title', 'title'], 'permissions': (('access', 'Access'), ('instructor', 'Instructor'), ('manage', 'Manager'))},
        ),
    ]
