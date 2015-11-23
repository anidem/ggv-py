# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0007_userworksheetstatus_can_check_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWorksheetScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('score', models.DecimalField(max_digits=5, decimal_places=2)),
                ('user', models.ForeignKey(related_name='user_scores', to=settings.AUTH_USER_MODEL)),
                ('worksheet', models.ForeignKey(related_name='worksheet_scores', to='questions.QuestionSet')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
