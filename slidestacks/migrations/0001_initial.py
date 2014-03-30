# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SlideStack'
        db.create_table(u'slidestacks_slidestack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Lesson'], null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Section'], null=True, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
            ('asset', self.gf('django.db.models.fields.CharField')(default='not specified', max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'slidestacks', ['SlideStack'])


    def backwards(self, orm):
        # Deleting model 'SlideStack'
        db.delete_table(u'slidestacks_slidestack')


    models = {
        u'lessons.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Subject'", 'max_length': '256'})
        },
        u'lessons.section': {
            'Meta': {'object_name': 'Section'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'slidestacks.slidestack': {
            'Meta': {'object_name': 'SlideStack'},
            'asset': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Lesson']", 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['slidestacks']