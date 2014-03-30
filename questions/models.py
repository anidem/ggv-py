from django.db import models
from django.core.urlresolvers import reverse

from lessons.models import Lesson, AbstractActivity


class QuestionSet(AbstractActivity):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, related_name='worksheets')

    def get_absolute_url(self):
        return reverse('worksheet', args=[str(self.id)])

    def __unicode__(self):
        return self.title


class QuestionResponse(models.Model):
    text = models.TextField()

    def __unicode__(self):
        return self.text


class AbstractQuestion(models.Model):
    text = models.TextField()
    display_order = models.IntegerField()

    def __unicode__(self):
        return self.text

    class Meta:
        abstract = True
        ordering = ['display_order']


class SimpleQuestion(AbstractQuestion):

    def get_absolute_url(self):
        return reverse('course', args=[str(self.id)])


class MultipleChoiceQuestion(AbstractQuestion):
    RADIO = 'radio'
    CHECK = 'checkbox'

    SELECTION_TYPES = (
        (RADIO, 'radio'),
        (CHECK, 'checkbox'),
    )

    select_type = models.CharField(
        max_length=24, choices=SELECTION_TYPES, default='radio')
    question_set = models.ForeignKey(QuestionSet, null=True)

    def getOptions(self):
        return QuestionOption.objects.filter(multiple_choice_question=self.id)

    def get_absolute_url(self):
        return reverse('multiplechoice', args=[str(self.id)])

    def __unicode__(self):
        return self.text


class QuestionOption(models.Model):
    text = models.CharField(max_length=512)
    correct = models.BooleanField(blank=True)
    multiple_choice_question = models.ForeignKey(
        MultipleChoiceQuestion, related_name='options', null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.text
