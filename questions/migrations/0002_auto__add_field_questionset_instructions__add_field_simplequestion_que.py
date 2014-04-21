# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QuestionSet.instructions'
        db.add_column(u'questions_questionset', 'instructions',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'SimpleQuestion.question_set'
        db.add_column(u'questions_simplequestion', 'question_set',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='simple_questions', null=True, to=orm['questions.QuestionSet']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'QuestionSet.instructions'
        db.delete_column(u'questions_questionset', 'instructions')

        # Deleting field 'SimpleQuestion.question_set'
        db.delete_column(u'questions_simplequestion', 'question_set_id')


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
        u'questions.multiplechoicequestion': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'MultipleChoiceQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mc_questions'", 'null': 'True', 'to': u"orm['questions.QuestionSet']"}),
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
            'Meta': {'ordering': "['section', 'display_order']", 'object_name': 'QuestionSet'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'worksheets'", 'null': 'True', 'to': u"orm['lessons.Lesson']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'questions.simplequestion': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'SimpleQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'simple_questions'", 'null': 'True', 'to': u"orm['questions.QuestionSet']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['questions']