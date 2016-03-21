# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20160320_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='ggv_organization',
            field=models.ForeignKey(related_name='organization_courses', to='courses.GGVOrganization', null=True),
            preserve_default=True,
        ),
    ]
