# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_control_worksheet_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='control_worksheet_results',
            field=models.BooleanField(default=False, choices=[(False, b'OPTION 1: Students are allowed to immediately review the results after completing a worksheet.'), (True, b'OPTION 2:  Students are NOT allowed to immediately review the results after completing a worksheet.')]),
            preserve_default=True,
        ),
    ]
