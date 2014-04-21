from django.db import models
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

from lessons.models import Lesson, AbstractActivity

class QuestionManager(models.Manager):
    
    def questions(self, **kwargs):
        sheet = QuestionSet.objects.get(pk=kwargs['id'])
        questions = sheet.questions.all().order_by('display_order')
        return questions


class QuestionSet(AbstractActivity):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, related_name='worksheets')
    activity_type = models.CharField(max_length=48, default='worksheet')

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

    def getOptions(self):
        return QuestionOption.objects.filter(question=self.id)

    def get_absolute_url(self):
        return reverse('question', args=[str(self.id)])

class QuestionOption(models.Model):
    text = models.CharField(max_length=512)
    correct = models.BooleanField(blank=True)
    question = models.ForeignKey(
        SimpleQuestion, related_name='options', null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.text

class QuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User)
    question = models.ForeignKey(SimpleQuestion)
    response = models.TextField()

    def __unicode__(self):
        return self.response
