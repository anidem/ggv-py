# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-21 05:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pretests', '0004_auto_20170220_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='PretestAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='pretestuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='pretestuser',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='pretests.PretestAccount'),
            preserve_default=False,
        ),
    ]
