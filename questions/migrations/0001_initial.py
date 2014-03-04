# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionResponse'
        db.create_table(u'questions_questionresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'questions', ['QuestionResponse'])

        # Adding model 'QuestionOption'
        db.create_table(u'questions_questionoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('correct', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'questions', ['QuestionOption'])

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
        ))
        db.send_create_signal(u'questions', ['MultipleChoiceQuestion'])

        # Adding M2M table for field options on 'MultipleChoiceQuestion'
        m2m_table_name = db.shorten_name(u'questions_multiplechoicequestion_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('multiplechoicequestion', models.ForeignKey(orm[u'questions.multiplechoicequestion'], null=False)),
            ('questionoption', models.ForeignKey(orm[u'questions.questionoption'], null=False))
        ))
        db.create_unique(m2m_table_name, ['multiplechoicequestion_id', 'questionoption_id'])


    def backwards(self, orm):
        # Deleting model 'QuestionResponse'
        db.delete_table(u'questions_questionresponse')

        # Deleting model 'QuestionOption'
        db.delete_table(u'questions_questionoption')

        # Deleting model 'SimpleQuestion'
        db.delete_table(u'questions_simplequestion')

        # Deleting model 'MultipleChoiceQuestion'
        db.delete_table(u'questions_multiplechoicequestion')

        # Removing M2M table for field options on 'MultipleChoiceQuestion'
        db.delete_table(db.shorten_name(u'questions_multiplechoicequestion_options'))


    models = {
        u'questions.multiplechoicequestion': {
            'Meta': {'object_name': 'MultipleChoiceQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['questions.QuestionOption']", 'symmetrical': 'False'}),
            'select_type': ('django.db.models.fields.CharField', [], {'default': "'radio'", 'max_length': '24'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'questions.questionoption': {
            'Meta': {'object_name': 'QuestionOption'},
            'correct': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'questions.questionresponse': {
            'Meta': {'object_name': 'QuestionResponse'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'questions.simplequestion': {
            'Meta': {'object_name': 'SimpleQuestion'},
            'display_order': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['questions']