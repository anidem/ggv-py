# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SlideStack.activity_type'
        db.alter_column(u'slidestacks_slidestack', 'activity_type', self.gf('django.db.models.fields.CharField')(max_length=48, null=True))

    def backwards(self, orm):

        # Changing field 'SlideStack.activity_type'
        db.alter_column(u'slidestacks_slidestack', 'activity_type', self.gf('django.db.models.fields.CharField')(max_length=48))

    models = {
        u'lessons.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Subject'", 'max_length': '256'})
        },
        u'lessons.section': {
            'Meta': {'ordering': "['title', 'display_order']", 'object_name': 'Section'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'slidestacks.slidestack': {
            'Meta': {'ordering': "['section', 'display_order']", 'object_name': 'SlideStack'},
            'activity_type': ('django.db.models.fields.CharField', [], {'default': "'slidestack'", 'max_length': '48', 'null': 'True'}),
            'asset': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'slidestacks'", 'null': 'True', 'to': u"orm['lessons.Lesson']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['slidestacks']