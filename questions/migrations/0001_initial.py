# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionSet'
        db.create_table(u'questions_questionset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Lesson'], null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Section'], null=True, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'questions', ['QuestionSet'])

        # Adding model 'QuestionResponse'
        db.create_table(u'questions_questionresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'questions', ['QuestionResponse'])

        # Adding model 'SimpleQuestion'
        db.create_table(u'questions_simplequestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'questions', ['SimpleQuestion'])

        # Adding model 'MultipleChoiceQuestion'
        db.create_table(u'questions_multiplechoicequestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
            ('select_type', self.gf('django.db.models.fields.CharField')(default='radio', max_length=24)),
            ('question_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.QuestionSet'], null=True)),
        ))
        db.send_create_signal(u'questions', ['MultipleChoiceQuestion'])

        # Adding model 'QuestionOption'
        db.create_table(u'questions_questionoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('correct', self.gf('django.db.models.fields.BooleanField')()),
            ('multiple_choice_question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', null=True, to=orm['questions.MultipleChoiceQuestion'])),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'questions', ['QuestionOption'])


    def backwards(self, orm):
        # Deleting model 'QuestionSet'
        db.delete_table(u'questions_questionset')

        # Deleting model 'QuestionResponse'
        db.delete_table(u'questions_questionresponse')

        # Deleting model 'SimpleQuestion'
        db.delete_table(u'questions_simplequestion')

        # Deleting model 'MultipleChoiceQuestion'
        db.delete_table(u'questions_multiplechoicequestion')

        # Deleting model 'QuestionOption'
        db.delete_table(u'questions_questionoption')


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
        u'questions.multiplechoicequestion': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'MultipleChoiceQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.QuestionSet']", 'null': 'True'}),
            'select_type': ('django.db.models.fields.CharField', [], {'default': "'radio'", 'max_length': '24'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'questions.questionoption': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'QuestionOption'},
            'correct': ('django.db.models.fields.BooleanField', [], {}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiple_choice_question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'null': 'True', 'to': u"orm['questions.MultipleChoiceQuestion']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'questions.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'questions.questionset': {
            'Meta': {'object_name': 'QuestionSet'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Lesson']", 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'questions.simplequestion': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'SimpleQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['questions']