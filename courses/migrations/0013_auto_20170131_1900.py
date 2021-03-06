# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-01 02:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_remove_course_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_courses', to='courses.Course')),
            ],
        ),
        migrations.AddField(
            model_name='coursetag',
            name='ggv_organization',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='organization_tags', to='courses.GGVOrganization'),
        ),
        migrations.AddField(
            model_name='taggedcourse',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged', to='courses.CourseTag'),
        ),
    ]
