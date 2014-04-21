# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MultipleChoiceQuestion'
        db.delete_table(u'questions_multiplechoicequestion')

        # Deleting field 'QuestionOption.multiple_choice_question'
        db.delete_column(u'questions_questionoption', 'multiple_choice_question_id')

        # Adding field 'QuestionOption.question'
        db.add_column(u'questions_questionoption', 'question',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', null=True, to=orm['questions.SimpleQuestion']),
                      keep_default=False)

        # Deleting field 'QuestionResponse.text'
        db.delete_column(u'questions_questionresponse', 'text')

        # Adding field 'QuestionResponse.user'
        db.add_column(u'questions_questionresponse', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'QuestionResponse.sheet'
        db.add_column(u'questions_questionresponse', 'sheet',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['questions.QuestionSet']),
                      keep_default=False)

        # Adding field 'QuestionResponse.item'
        db.add_column(u'questions_questionresponse', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['questions.SimpleQuestion']),
                      keep_default=False)

        # Adding field 'QuestionResponse.response'
        db.add_column(u'questions_questionresponse', 'response',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'SimpleQuestion.select_type'
        db.add_column(u'questions_simplequestion', 'select_type',
                      self.gf('django.db.models.fields.CharField')(default='radio', max_length=24),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'MultipleChoiceQuestion'
        db.create_table(u'questions_multiplechoicequestion', (
            ('select_type', self.gf('django.db.models.fields.CharField')(default='radio', max_length=24)),
            ('question_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mc_questions', null=True, to=orm['questions.QuestionSet'])),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'questions', ['MultipleChoiceQuestion'])

        # Adding field 'QuestionOption.multiple_choice_question'
        db.add_column(u'questions_questionoption', 'multiple_choice_question',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', null=True, to=orm['questions.MultipleChoiceQuestion']),
                      keep_default=False)

        # Deleting field 'QuestionOption.question'
        db.delete_column(u'questions_questionoption', 'question_id')

        # Adding field 'QuestionResponse.text'
        db.add_column(u'questions_questionresponse', 'text',
                      self.gf('django.db.models.fields.TextField')(default='blank'),
                      keep_default=False)

        # Deleting field 'QuestionResponse.user'
        db.delete_column(u'questions_questionresponse', 'user_id')

        # Deleting field 'QuestionResponse.sheet'
        db.delete_column(u'questions_questionresponse', 'sheet_id')

        # Deleting field 'QuestionResponse.item'
        db.delete_column(u'questions_questionresponse', 'item_id')

        # Deleting field 'QuestionResponse.response'
        db.delete_column(u'questions_questionresponse', 'response')

        # Deleting field 'SimpleQuestion.select_type'
        db.delete_column(u'questions_simplequestion', 'select_type')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        u'questions.questionoption': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'QuestionOption'},
            'correct': ('django.db.models.fields.BooleanField', [], {}),
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'null': 'True', 'to': u"orm['questions.SimpleQuestion']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'questions.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.SimpleQuestion']"}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.QuestionSet']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'null': 'True', 'to': u"orm['questions.QuestionSet']"}),
            'select_type': ('django.db.models.fields.CharField', [], {'default': "'radio'", 'max_length': '24'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['questions']