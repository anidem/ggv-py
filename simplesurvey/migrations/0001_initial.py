# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-06 22:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyOptionQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
                ('response_required', models.BooleanField(default=False)),
                ('input_select', models.CharField(choices=[('radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio', max_length=64)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_option_questions', to='simplesurvey.Survey')),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.CharField(max_length=256)),
                ('display_order', models.IntegerField(default=0)),
                ('survey_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question_options', to='simplesurvey.SurveyOptionQuestion')),
            ],
            options={
                'ordering': ['display_order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('response', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question_responses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyTextQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
                ('response_required', models.BooleanField(default=False)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_text_questions', to='simplesurvey.Survey')),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
        ),
    ]
