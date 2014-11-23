from django.db import models
from django.db.models import Count
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django import forms
from operator import itemgetter
import json

from model_utils.models import TimeStampedModel

from lessons.models import Lesson, AbstractActivity
from notes.models import UserNote


class QuestionManager(models.Manager):

    def worksheet_report(self, **kwargs):
        report = []

        try:
            user = kwargs.pop('user')
            questions = self.questions(id=kwargs.pop('worksheet').id)
        except:
            return report

        for q in questions:
            obj = {}
            obj['question'] = q
            try:
                obj['response'] = q.responses.get(user=user)
                obj['correct']  = (obj['response'].response in q.get_correct_answer())
            except:
                obj['response'] = None
                obj['correct'] = None                

            report.append(obj)
        
        return report

    def questions(self, **kwargs):
        set_id = kwargs.pop('id')
        sheet = QuestionSet.objects.get(pk=set_id)
        mc_questions = sheet.shortanswerquestions.all().order_by(
            'display_order')
        sa_questions = sheet.multiplechoicequestions.all().order_by(
            'display_order')
        questions = sorted(
            chain(mc_questions, sa_questions),
            key=attrgetter('display_order')
        )
        return questions

    def user_worksheet(self, **kwargs):
        user_id = kwargs.pop('user')
        worksheet_id = kwargs.pop('id')
        user = User.objects.get(pk=user_id)
        sheet = QuestionSet.objects.get(pk=worksheet_id)

        questions = self.questions(id=worksheet_id)
        # response object is {QUESTION} {RESPONSE} {OPTION_LIST [OPTIONS]}

        question_response_list = []
        for q in questions:
            response_obj = dict()
            # Record question
            response_obj['question_obj'] = q
            response_obj['question_id'] = q.id
            response_obj['question_text'] = q.text
            response_obj[
                'question_type'] = q.get_question_content_type().id

            # Record previous response if it exists
            response_obj['response'] = None
            response_obj['correct'] = False

            try:
                response_obj['response'] = q.responses.get(user=user)
                if response_obj['response'].response in q.correct_answer:
                    response_obj['correct'] = True
                    
            except:
                pass

            # Record question options if they exist
            option_obj_list = []
            for opt in q.get_options():
                option_obj = []
                option_obj.append(opt.text)
                option_obj.append(opt.text)
                if response_obj['response']:
                    if opt.text == response_obj['response'].response:
                        # option_obj['response'] = response_obj['response']
                        response_obj['correct'] = opt.is_correct
                    
                option_obj_list.append(option_obj)
            
            response_obj['options'] = option_obj_list

            question_response_list.append(response_obj)
        return question_response_list


class QuestionSet(AbstractActivity):
    lesson = models.ForeignKey(
        Lesson, null=True, blank=True, related_name='worksheets')
    activity_type = models.CharField(
        max_length=48, default='worksheet', null=True)
    notes = GenericRelation(UserNote)

    # objects = QuestionManager()

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.lesson in user_session['user_lessons']

    def get_ordered_question_list(self):
        seqitems = [(x.content_object, x.content_object.display_order) for x in self.sequence_items.all()]
        return [x[0] for x in sorted(seqitems, key=itemgetter(1))]

    def get_absolute_url(self):
        return reverse('question_response', args=[self.id, '1'])

    def __unicode__(self):
        return self.title


class QuestionSequenceItem(models.Model):

    """
    Functions as a list of questions for QuestionSet.
    Allow QuestionSets to contain varied question types.
    Content objects reference types derived from Abstract Question.
    """
    question_sequence = models.ForeignKey(
        QuestionSet, related_name='sequence_items')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class AbstractQuestion(models.Model):

    """
    A super class specifying the question text to display and the display order of the question.
    """
    display_text = models.TextField()
    display_order = models.IntegerField(default=0)
    display_image = models.FileField(null=True, blank=True, upload_to='img')

    def get_sequence_url(self):
        try:
            seqitem = self.sequence.all()[0]
            print 'seqitem', seqitem
            worksheet = seqitem.question_sequence
            position = worksheet.get_ordered_question_list().index(self)
            
            return reverse('question_response', args=[worksheet.id, position+1])
        except Exception as inst:
            print inst
            return None

    def __unicode__(self):
        return self.display_text

    class Meta:
        abstract = True
        ordering = ['display_order']


class TextQuestion(AbstractQuestion):

    """
    A question type that accepts text input.
    """
    input_size = models.CharField(max_length=64, choices=[
        ('1', 'short answer: (1 row 50 cols)'),
        ('5', 'sentence: (5 rows 50 cols'),
        ('15', 'paragraph(s): (15 rows 50 cols)')], default='1')
    correct = models.TextField(blank=True)
    sequence = GenericRelation(
        QuestionSequenceItem, related_query_name='questions')
    responses = GenericRelation('QuestionResponse')
    notes = GenericRelation(UserNote)

    def get_input_widget(self):
        widget_attrs = {
            'rows': self.input_size,
            'cols': 50,
            'style': 'resize: vertical'
        }
        if self.input_size == '1':
            return forms.CharField(label='', widget=forms.TextInput(attrs={'size': 50}))
        else:
            return forms.CharField(label='', widget=forms.Textarea(attrs=widget_attrs))

    def correct_answer(self):
        return self.correct

    def check_answer(self, json_str):
        return json_str == self.correct

    def user_response_object(self, user):        
        """
        Returns a QuestionResponse object related to user.
        """
        try:
            return self.responses.all().get(user=user)
        except:
            return None

    def get_edit_url(self):
        return reverse('text_question_update', args=[self.id])

    def get_absolute_url(self):
        return reverse('text_question', args=[self.id])



class OptionQuestion(AbstractQuestion):

    """
    A question type that accepts a selection from a list of choices (multiple choice).
    """
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')

    sequence = GenericRelation(
        QuestionSequenceItem, related_query_name='questions')
    responses = GenericRelation('QuestionResponse')
    notes = GenericRelation(UserNote)

    def get_input_widget(self):
        if self.input_select == 'checkbox':
            field_widget = forms.CheckboxSelectMultiple()
            return forms.MultipleChoiceField(label='', choices=self.options_list(), widget=field_widget)
        else:
            field_widget = forms.RadioSelect()
            return forms.ChoiceField(label='', choices=self.options_list(), widget=field_widget)

    def options_list(self):
        return [(i.id, i.display_text) for i in self.options.all()]

    def correct_answer(self):
        if self.input_select == 'checkbox':
            return [str(i.id) for i in self.options.filter(correct=True)]
        else:
            return str(self.options.get(correct=True).id)

    def check_answer(self, json_str):
        # Need to process option responses as lists. json used to coerce
        # string representation to list.
        try:
            return self.correct_answer() == json_str
        except:
            print 'error doing json compare check'

    def user_response_object(self, user):
        """
        Returns a QuestionResponse object related to user.
        """
        try:
            return self.responses.get(user=user)
        except:
            return None

    def get_edit_url(self):
        return reverse('option_question_update', args=[self.id])

    def get_absolute_url(self):
        return reverse('option_question', args=[self.id])

class Option(models.Model):

    """
    Stores a single option to list as a choice for a :model:`questions.OptionQuestion`.
    """
    question = models.ForeignKey(OptionQuestion, related_name='options')
    correct = models.BooleanField(default=False)
    display_text = models.CharField(max_length=256)
    display_order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.display_text

    class Meta:
        ordering = ['display_order', 'id']


class QuestionResponse(TimeStampedModel):
    """
    Generic question response container.
    Designed to reference objects derived from AbstractQuestion (e.g., OptionQuestion, TextQuestion) 
    """
    user = models.ForeignKey(User, related_name='question_responses')
    response = models.TextField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def json_response(self):
        try:
            return json.loads(self.response)
        except:
            return None        

    def save(self, *args, **kwargs):
        self.response = json.dumps(self.response)
        super(QuestionResponse, self).save(*args, **kwargs)

    # Fix this to contruct arguments relative to question sequence object
    def get_absolute_url(self):
        return reverse('home')
