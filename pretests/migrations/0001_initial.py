# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-18 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PretestQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('response', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('iscorrect', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='PretestUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('access_token', models.CharField(max_length=512)),
                ('expired', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='pretestquestionresponse',
            name='pretestuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pretest_responses', to='pretests.PretestUser'),
        ),
        migrations.AlterUniqueTogether(
            name='pretestquestionresponse',
            unique_together=set([('pretestuser', 'object_id', 'content_type')]),
        ),
    ]
