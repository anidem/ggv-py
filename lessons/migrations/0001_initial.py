# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lesson'
        db.create_table(u'lessons_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Subject', max_length=256)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'lessons', ['Lesson'])

        # Adding model 'Activity'
        db.create_table(u'lessons_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('assets', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Lesson'], null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Section'], null=True, blank=True)),
        ))
        db.send_create_signal(u'lessons', ['Activity'])

        # Adding model 'Section'
        db.create_table(u'lessons_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'lessons', ['Section'])


    def backwards(self, orm):
        # Deleting model 'Lesson'
        db.delete_table(u'lessons_lesson')

        # Deleting model 'Activity'
        db.delete_table(u'lessons_activity')

        # Deleting model 'Section'
        db.delete_table(u'lessons_section')


    models = {
        u'lessons.activity': {
            'Meta': {'object_name': 'Activity'},
            'assets': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Lesson']", 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'lessons.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Subject'", 'max_length': '256'})
        },
        u'lessons.section': {
            'Meta': {'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['lessons']