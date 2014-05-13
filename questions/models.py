from django.db import models
from django.db.models import Count
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

from lessons.models import Lesson, AbstractActivity

class QuestionManager(models.Manager):
    
    def worksheet(self, **kwargs):
        print '%s:%s' % ('USER', kwargs['user'])
        questions = SimpleQuestion.objects.filter(question_set=kwargs['id']).order_by('display_order')
        responses = QuestionResponse.objects.filter(user__id=kwargs['user']).filter(worksheet__id=kwargs['id'])

        return responses      

    def questions(self, **kwargs):
        sheet = QuestionSet.objects.get(pk=kwargs['id'])
        questions = sheet.questions.all().order_by('display_order')
        return questions

    def user_worksheet(self, **kwargs):
        user = User.objects.get(pk=kwargs['user'])
        questions = SimpleQuestion.objects.filter(question_set=kwargs['id']).order_by('display_order')
        user_responses = QuestionResponse.objects.filter(user__id=kwargs['user'])
        question_response_list = []
        for q in questions:
            response_obj = dict()
            response_obj['question'] = q
            response_obj['options'] = q.get_options()
            response_obj['user_response'] = user_responses.get(question=q) or None
            question_response_list.append(response_obj)
        return question_response_list

class QuestionSet(AbstractActivity):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, related_name='worksheets')
    activity_type = models.CharField(max_length=48, default='worksheet', null=True)

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('worksheet', args=[str(self.id)])

    def __unicode__(self):
        return self.title


class AbstractQuestion(models.Model):
    text = models.TextField()
    display_order = models.IntegerField()

    def __unicode__(self):
        return self.text

    class Meta:
        abstract = True
        ordering = ['display_order']

class SimpleQuestion(AbstractQuestion):
    RADIO = 'radio'
    CHECK = 'checkbox'
    TEXT = 'text'

    SELECTION_TYPES = (
        (RADIO, 'radio'),
        (CHECK, 'checkbox'),
        (TEXT, 'text'),
    )

    select_type = models.CharField(
        max_length=24, choices=SELECTION_TYPES, default='radio')
    question_set = models.ForeignKey(QuestionSet, null=True, related_name='questions')
    correct_answer = models.TextField(null=True, blank=True)

    def get_options(self):
        return QuestionOption.objects.filter(question=self.id).order_by('display_order')

    def get_absolute_url(self):
        return reverse('question', args=[str(self.id)])

class QuestionOption(models.Model):
    text = models.CharField(max_length=512)
    is_correct = models.BooleanField(blank=True, default=False)
    question = models.ForeignKey(
        SimpleQuestion, related_name='options')
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.text

class QuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User)
    worksheet = models.ForeignKey(QuestionSet)
    question = models.ForeignKey(SimpleQuestion)
    response = models.TextField()

    def __unicode__(self):
        return self.response
