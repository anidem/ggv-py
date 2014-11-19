# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('display_order', models.IntegerField()),
                ('select_type', models.CharField(default=b'radio', max_length=24, choices=[(b'radio', b'radio'), (b'checkbox', b'checkbox')])),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=512)),
                ('is_correct', models.BooleanField(default=False)),
                ('display_order', models.IntegerField(default=0)),
                ('question', models.ForeignKey(related_name=b'options', to='questions.MultipleChoiceQuestion')),
            ],
            options={
                'ordering': ['display_order'],
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
                ('question_id', models.PositiveIntegerField(null=True)),
                ('question_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('lesson', models.ForeignKey(related_name=b'worksheets', blank=True, to='lessons.Lesson', null=True)),
                ('section', models.ForeignKey(blank=True, to='lessons.Section', null=True)),
            ],
            options={
                'ordering': ['section', 'display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShortAnswerQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('display_order', models.IntegerField()),
                ('correct_answer', models.CharField(max_length=256)),
                ('question_set', models.ForeignKey(related_name=b'shortanswerquestions', to='questions.QuestionSet')),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='question_set',
            field=models.ForeignKey(related_name=b'multiplechoicequestions', to='questions.QuestionSet', null=True),
            preserve_default=True,
        ),
    ]
