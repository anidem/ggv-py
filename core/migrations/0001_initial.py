# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'core_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('access_code', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Course'])

        # Adding M2M table for field lessons on 'Course'
        m2m_table_name = db.shorten_name(u'core_course_lessons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'core.course'], null=False)),
            ('lesson', models.ForeignKey(orm[u'lessons.lesson'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'lesson_id'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'core_course')

        # Removing M2M table for field lessons on 'Course'
        db.delete_table(db.shorten_name(u'core_course_lessons'))


    models = {
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'access_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'associated_courses'", 'symmetrical': 'False', 'to': u"orm['lessons.Lesson']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'lessons.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Subject'", 'max_length': '256'})
        }
    }

    complete_apps = ['core']