# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correct', models.BooleanField(default=False)),
                ('display_text', models.CharField(max_length=256)),
                ('display_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['display_order', 'id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
                ('display_image', models.FileField(null=True, upload_to=b'img', blank=True)),
                ('input_select', models.CharField(default=b'radio', max_length=64, choices=[(b'radio', b'single responses'), (b'checkbox', b'multiple responses')])),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('response', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='question_responses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('instructions', models.TextField(null=True)),
                ('display_order', models.IntegerField()),
                ('activity_type', models.CharField(default=b'worksheet', max_length=48, null=True)),
                ('lesson', models.ForeignKey(related_name='worksheets', blank=True, to='lessons.Lesson', null=True)),
                ('section', models.ForeignKey(blank=True, to='lessons.Section', null=True)),
            ],
            options={
                'ordering': ['section', 'display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
                ('display_image', models.FileField(null=True, upload_to=b'img', blank=True)),
                ('input_size', models.CharField(default=b'1', max_length=64, choices=[(b'1', b'short answer: (1 row 50 cols)'), (b'5', b'sentence: (5 rows 50 cols'), (b'15', b'paragraph(s): (15 rows 50 cols)')])),
                ('correct', models.TextField(blank=True)),
                ('question_set', models.ForeignKey(related_name='text_questions', to='questions.QuestionSet')),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWorksheetStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('completed_worksheet', models.ForeignKey(to='questions.QuestionSet')),
                ('user', models.ForeignKey(related_name='completed_worksheets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='question_set',
            field=models.ForeignKey(related_name='option_questions', to='questions.QuestionSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(related_name='options', to='questions.OptionQuestion'),
            preserve_default=True,
        ),
    ]
