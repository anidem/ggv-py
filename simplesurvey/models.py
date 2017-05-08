from __future__ import unicode_literals

from itertools import chain
from operator import attrgetter

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from model_utils.models import TimeStampedModel


class Survey(models.Model):
    title = models.CharField(max_length=255)
    
    def get_ordered_question_list(self):
        """Should return a list of questions (text and option) in specified display order."""
        option_questions = self.survey_option_questions.all()
        text_questions = self.survey_text_questions.all()
        
        questions = sorted(
            chain(option_questions, text_questions),
            key=attrgetter('display_order')
        )
        return questions
        

class AbstractSurveyQuestion(models.Model):
    display_text = models.TextField()
    display_order = models.IntegerField(default=0)
    response_required = models.BooleanField(default=False)

    def __unicode__(self):
        return self.display_text

    class Meta:
        abstract = True
        ordering = ['display_order']


class SurveyTextQuestion(AbstractSurveyQuestion):

    """
    A question type that accepts text input.
    """

    survey = models.ForeignKey(Survey, related_name='survey_text_questions')
    responses = GenericRelation('SurveyQuestionResponse')

    def get_question_type(self):
        return 'text'

    def get_django_content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_input_widget(self):
        widget_attrs = {
            'rows': 15,
            'cols': 40,
            'style': 'resize: vertical'
        }
        return forms.CharField(label='', widget=forms.Textarea(attrs=widget_attrs))         

    def get_absolute_url(self):
        pass
        # return reverse('text_question', args=[self.id])


class SurveyOptionQuestion(AbstractSurveyQuestion):

    """
    A question type that accepts a selection from a list of choices (multiple choice).
    """  
    survey = models.ForeignKey(Survey, related_name='survey_option_questions')
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')
    responses = GenericRelation('SurveyQuestionResponse')
    
    def get_question_type(self):
        return 'option'

    def get_django_content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_input_widget(self):
        if self.input_select == 'checkbox':
            field_widget = forms.CheckboxSelectMultiple()
            return forms.MultipleChoiceField(label='', choices=self.options_list(), widget=field_widget)
        else:
            field_widget = forms.RadioSelect()
            return forms.ChoiceField(label='', choices=self.options_list(), widget=field_widget)

    def options_list(self):
        return [(i.id, i.display_text) for i in self.survey_question_options.all()]

    def get_absolute_url(self):
        # return reverse('option_question', args=[self.id])
        pass


class SurveyQuestionOption(models.Model):
    """
    Stores a single option to list as a choice for a :model:`questions.OptionQuestion`.
    """
    survey_question = models.ForeignKey(SurveyOptionQuestion, related_name='survey_question_options')
    display_text = models.CharField(max_length=256)
    display_order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.display_text

    class Meta:
        ordering = ['display_order', 'id']


class SurveyQuestionResponse(TimeStampedModel):

    """
    Generic question response container.
    Designed to reference objects derived from AbstractQuestion (e.g., OptionQuestion, TextQuestion)
    """

    user = models.ForeignKey(User, related_name='survey_question_responses')
    response = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def json_response(self):
        try:
            return json.loads(self.response)
        except:
            return self.response

    def get_question_object(self):
        return self.content_object

    def save(self, *args, **kwargs):
        """
        The response is always stored as a json string if its a checkbox input. Any read operation must decode the response:
        E.g., json.loads(response) See: self.json_response() method.

        Every save operation will update the iscorrect field.
        """
        if self.content_object.get_question_type() == 'option' and self.content_object.input_select == 'checkbox':
            try:  # verify that response is not already encoded in json
                json.loads(self.response)
            except Exception as e:
                # print "DUMPING TO JSON==>:", json.dumps(ast.literal_eval(self.response))
                self.response = json.dumps(ast.literal_eval(self.response)) # previous: json.dumps(self.response)
                        
        super(SurveyQuestionResponse, self).save(*args, **kwargs)        

    def get_absolute_url(self):
        pass
        # return reverse('home')
