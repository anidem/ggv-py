# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20160303_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='GGVOrganization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('user_quota', models.IntegerField(default=0)),
                ('quota_start_date', models.DateField()),
                ('business_contact_email', models.EmailField(max_length=75)),
                ('business_contact_phone', models.CharField(max_length=12)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='course',
            name='ggv_organization',
            field=models.ForeignKey(to='courses.GGVOrganization', null=True),
            preserve_default=True,
        ),
    ]
