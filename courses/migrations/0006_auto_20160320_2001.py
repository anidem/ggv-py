# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20160320_1958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['ggv_organization', 'title'], 'permissions': (('access', 'Access'), ('instructor', 'Instructor'), ('manage', 'Manager'))},
        ),
        migrations.AlterModelOptions(
            name='ggvorganization',
            options={'ordering': ['title']},
        ),
    ]
