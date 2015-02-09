# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernote',
            name='course_context',
            field=models.ForeignKey(blank=True, to='courses.Course', null=True),
            preserve_default=True,
        ),
    ]
