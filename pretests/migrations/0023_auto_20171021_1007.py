# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-21 16:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pretests', '0022_pretestaccount_tests_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pretestaccount',
            name='ggv_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pretest_account_associations', to='courses.GGVOrganization'),
        ),
        migrations.AlterField(
            model_name='pretestaccount',
            name='tokens_purchased',
            field=models.PositiveIntegerField(default=0, help_text='We no longer use this. Customers purchase Tests and assign them as needed.'),
        ),
    ]
