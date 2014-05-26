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
            ('instructions', self.gf('django.db.models.fields.TextField')(null=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lessons.Section'], null=True, blank=True)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='worksheets', null=True, to=orm['lessons.Lesson'])),
            ('activity_type', self.gf('django.db.models.fields.CharField')(default='worksheet', max_length=48, null=True)),
        ))
        db.send_create_signal(u'questions', ['QuestionSet'])

        # Adding model 'ShortAnswerQuestion'
        db.create_table(u'questions_shortanswerquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
            ('question_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shortanswerquestions', null=True, to=orm['questions.QuestionSet'])),
        ))
        db.send_create_signal(u'questions', ['ShortAnswerQuestion'])

        # Adding model 'MultipleChoiceQuestion'
        db.create_table(u'questions_multiplechoicequestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('display_order', self.gf('django.db.models.fields.IntegerField')()),
            ('select_type', self.gf('django.db.models.fields.CharField')(default='radio', max_length=24)),
            ('question_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='multiplechoicequestions', null=True, to=orm['questions.QuestionSet'])),
        ))
        db.send_create_signal(u'questions', ['MultipleChoiceQuestion'])

        # Adding model 'QuestionOption'
        db.create_table(u'questions_questionoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['questions.MultipleChoiceQuestion'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('is_correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'questions', ['QuestionOption'])

        # Adding model 'QuestionResponse'
        db.create_table(u'questions_questionresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('response', self.gf('django.db.models.fields.TextField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'questions', ['QuestionResponse'])


    def backwards(self, orm):
        # Deleting model 'QuestionSet'
        db.delete_table(u'questions_questionset')

        # Deleting model 'ShortAnswerQuestion'
        db.delete_table(u'questions_shortanswerquestion')

        # Deleting model 'MultipleChoiceQuestion'
        db.delete_table(u'questions_multiplechoicequestion')

        # Deleting model 'QuestionOption'
        db.delete_table(u'questions_questionoption')

        # Deleting model 'QuestionResponse'
        db.delete_table(u'questions_questionresponse')


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
            'Meta': {'ordering': "['lesson', 'display_order', 'title']", 'object_name': 'Section'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Lesson']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'questions.multiplechoicequestion': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'MultipleChoiceQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'multiplechoicequestions'", 'null': 'True', 'to': u"orm['questions.QuestionSet']"}),
            'select_type': ('django.db.models.fields.CharField', [], {'default': "'radio'", 'max_length': '24'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'questions.questionoption': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'QuestionOption'},
            'display_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': u"orm['questions.MultipleChoiceQuestion']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'questions.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'questions.questionset': {
            'Meta': {'ordering': "['section', 'display_order']", 'object_name': 'QuestionSet'},
            'activity_type': ('django.db.models.fields.CharField', [], {'default': "'worksheet'", 'max_length': '48', 'null': 'True'}),
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'worksheets'", 'null': 'True', 'to': u"orm['lessons.Lesson']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lessons.Section']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'questions.shortanswerquestion': {
            'Meta': {'ordering': "['display_order']", 'object_name': 'ShortAnswerQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shortanswerquestions'", 'null': 'True', 'to': u"orm['questions.QuestionSet']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['questions']