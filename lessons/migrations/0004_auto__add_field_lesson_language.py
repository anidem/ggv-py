# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lesson.language'
        db.add_column(u'lessons_lesson', 'language',
                      self.gf('django.db.models.fields.CharField')(default='eng', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Lesson.language'
        db.delete_column(u'lessons_lesson', 'language')


    models = {
        u'lessons.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'icon_class': ('django.db.models.fields.CharField', [], {'default': "'university'", 'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'eng'", 'max_length': '32'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Subject'", 'max_length': '256'})
        },
        u'lessons.section': {
            'Meta': {'ordering': "['lesson', 'display_order', 'title']", 'object_name': 'Section'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['lessons.Lesson']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['lessons']