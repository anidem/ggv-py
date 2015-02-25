# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_coursepermission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': (('access', 'Access'), ('instructor', 'Instructor'), ('manage', 'Manager'))},
        ),
        migrations.AlterField(
            model_name='coursepermission',
            name='course',
            field=models.ForeignKey(related_name='course_permissions', to='courses.Course'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coursepermission',
            name='user',
            field=models.ForeignKey(related_name='user_course_permissions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
