from django.db import models
from django.db.models import Count
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


from model_utils.models import TimeStampedModel

from lessons.models import Lesson, AbstractActivity

class QuestionManager(models.Manager):
    
    # def worksheet(self, **kwargs):
    #     print '%s:%s' % ('USER', kwargs['user'])
    #     set_id = kwargs.pop('id')
    #     questions = MultipleChoiceQuestion.objects.filter(question_set=set_id).order_by('display_order')
    #     responses = QuestionResponse.objects.filter(user__id=kwargs['user']).filter(worksheet__id=set_id)

    #     return responses      

    def questions(self, **kwargs):
        set_id = kwargs.pop('id')
        sheet = QuestionSet.objects.get(pk=set_id)
        mc_questions = sheet.shortanswerquestions.all().order_by('display_order')
        sa_questions = sheet.multiplechoicequestions.all().order_by('display_order')
        
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
        
        mc_questions = sheet.shortanswerquestions.all().order_by('display_order')
        sa_questions = sheet.multiplechoicequestions.all().order_by('display_order')
        
        questions = sorted(
            chain(mc_questions, sa_questions),
            key=attrgetter('display_order')
            )

        user_responses = QuestionResponse.objects.filter(user__id=user.id)
        question_response_list = []

        
        for q in questions:
            response_obj = dict()
            option_obj_list = []
            response_obj['question'] = q
            try:
                response_obj['user_response'] = user_responses.get(question=q)
            except:
                response_obj['user_response'] = None
            
            for opt in q.get_options():
                option_obj = dict()
                option_obj['option'] = opt
                if response_obj['user_response'] and opt.text == response_obj['user_response'].response:
                    option_obj['response'] = response_obj['user_response']
                else:
                    option_obj['response'] = None
                
                option_obj_list.append(option_obj)
            
            response_obj['options'] = option_obj_list
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

class ShortAnswerQuestion(AbstractQuestion):    
    correct_answer = models.TextField()
    question_set = models.ForeignKey(QuestionSet, related_name='shortanswerquestions')


    def get_options(self):
        return []

    def get_correct_answer(self):
        return correct_answer

    def get_question_type(self):
        return 'shortanswerquestion'


class MultipleChoiceQuestion(AbstractQuestion):
    RADIO = 'radio'
    CHECK = 'checkbox'

    OPTION_TYPES = (
        (RADIO, 'radio'),
        (CHECK, 'checkbox'),
    )

    select_type = models.CharField(
        max_length=24, choices=OPTION_TYPES, default=RADIO)
    question_set = models.ForeignKey(QuestionSet, null=True, related_name='multiplechoicequestions')

    def get_options(self):
        return QuestionOption.objects.filter(question=self.id).order_by('display_order')

    def get_correct_answer(self):
        return QuestionOption.objects.filter(question=self.id).filter(is_correct=True).order_by('display_order')

    def get_question_type(self):
        return 'multiplechoicequestion'

class QuestionOption(models.Model):
    question = models.ForeignKey(
        MultipleChoiceQuestion, related_name='options')
    text = models.CharField(max_length=512)
    is_correct = models.BooleanField(blank=True, default=False)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.text

class QuestionResponse(TimeStampedModel):
    user = models.ForeignKey(User)
    response = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.response
