# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('questions', '0001_initial'),
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
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OptionQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
                ('input_select', models.CharField(default=b'radio', max_length=64, choices=[(b'radio', b'single responses'), (b'checkbox', b'multiple responses')])),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionSequenceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('question_sequence', models.ForeignKey(related_name=b'questions', to='questions.QuestionSet')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
                ('input_size', models.CharField(default=b'1', max_length=64, choices=[(b'1', b'short answer: (1 row 80 cols)'), (b'5', b'sentence: (5 rows 80 cols'), (b'15', b'paragraph(s): (15 rows 80 cols)')])),
                ('correct', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['display_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='question_set',
        ),
        migrations.RemoveField(
            model_name='questionoption',
            name='question',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceQuestion',
        ),
        migrations.DeleteModel(
            name='QuestionOption',
        ),
        migrations.RemoveField(
            model_name='shortanswerquestion',
            name='question_set',
        ),
        migrations.DeleteModel(
            name='ShortAnswerQuestion',
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(related_name=b'options', to='questions.OptionQuestion'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='questionresponse',
            old_name='question_type',
            new_name='content_type',
        ),
        migrations.RemoveField(
            model_name='questionresponse',
            name='question_id',
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='user',
            field=models.ForeignKey(related_name=b'question_responses', to=settings.AUTH_USER_MODEL),
        ),
    ]
