from django.db import models
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django import forms
import json

from model_utils.models import TimeStampedModel

from lessons.models import Lesson, AbstractActivity
from notes.models import UserNote
from core.models import Bookmark

class QuestionSet(AbstractActivity):
    lesson = models.ForeignKey(
        Lesson, null=True, blank=True, related_name='worksheets')
    activity_type = models.CharField(
        max_length=48, default='worksheet', null=True)
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)
    display_pdf = models.FileField(null=True, blank=True, upload_to='pdf')

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.lesson in user_session['user_lessons']

    def get_question_at_index(self, index):
        try:
            question = self.get_ordered_question_list()[index]
            return {'index': index, 'question': question}
        except:
            return None

    def get_ordered_question_list(self):
        option_questions = self.option_questions.all()
        text_questions = self.text_questions.all()
        questions = sorted(
            chain(option_questions, text_questions),
            key=attrgetter('display_order')
        )
        return questions

    def get_num_questions(self):
        return len(self.get_ordered_question_list())

    def get_next_question(self, user):
        questions = self.get_ordered_question_list()
        index = 1
        for i in questions:
            if not i.user_response_object(user):
                return {'index': index, 'question': i}
            index = index + 1
        return None

    def get_user_responses(self, user, questions, course):
        report = []
        bookmarks = Bookmark.objects.filter(
            creator=user).filter(course_context=course)
        numcorrect = 0
        for i in questions:
            question_type = ContentType.objects.get_for_model(i)
            bookmark = bookmarks.filter(
                content_type=question_type.id).filter(object_id=i.id)
            bk = None
            if bookmark:
                bk = bookmark[0]
            response = None
            respobj = i.user_response_object(user)
            if respobj:
                # resp = respobj.response.replace('"', '')
                resp = json.loads(respobj.response)

                if question_type.name == 'option question':
                    if i.input_select == 'checkbox': # dealing with a list of responses/answers
                        try:
                            r = {int(x) for x in resp} # create response list as a set
                            a = {int(x) for x in i.correct_answer()} # retrieve the answer list as a set

                            score = True
                            if a - r: # find diff between sets. if not empty (diffs exist) score is false
                                score = False

                                # Build a string out of the response list
                            respstr = [str('(%s)')%Option.objects.get(pk=x).display_text for x in list(r)]
                            resp = ', '.join(respstr)
                        except:
                            score = False
                            resp = 'This question may have been modified. Please re-answer or report problem to instructor.'

                    else:
                        try:
                            r = int(resp)
                            score = r in i.correct_answer()
                            resp = Option.objects.get(pk=r).display_text
                        except:
                            score = False
                            resp = 'This question may have been modified. Please re-answer or report problem to instructor.'

                else:
                    # Check if text question has correct answer specified. count it if null.
                    if not i.correct:
                        score = True
                    else:
                        score = i.correct_answer() == resp

                if score:
                    numcorrect = numcorrect + 1

                response = (bk, i, resp, score)  # str(i.correct_answer())
                report.append(response)

        grade = float(numcorrect)/len(questions)*100

        return {'report': report, 'correct': numcorrect, 'grade': grade}

    def get_all_responses(self, course):
        members = course.member_list()
        questions = self.get_ordered_question_list()
        report = []
        for i in members:
            user_report = self.get_user_responses(i, questions, course)
            responses = user_report['report']
            correct = user_report['correct']
            grade = user_report['grade']

            report.append((i, responses, correct, grade))

        return report

    def get_absolute_url(self):
        return reverse('question_response', args=[self.id, '1'])

    def __unicode__(self):
        return self.title


class AbstractQuestion(models.Model):

    """
    A super class specifying the question text to display and the display order of the question.
    """
    display_text = models.TextField()
    display_order = models.IntegerField(default=0)
    display_image = models.FileField(null=True, blank=True, upload_to='img')
    display_pdf = models.FileField(null=True, blank=True, upload_to='pdf')
    display_key_file = models.FileField(null=True, blank=True, upload_to='pdf')
    response_required = models.BooleanField(default=True)

    def get_sequence_url(self, course):
        try:
            position = self.question_set.get_ordered_question_list().index(
                self)
            return reverse('question_response', args=[course.slug, self.question_set.id, position + 1])
        except Exception:
            return None

    def __unicode__(self):
        return self.display_text

    class Meta:
        abstract = True
        ordering = ['display_order']

# class NoResponseQuestion(AbstractQuestion):



class TextQuestion(AbstractQuestion):

    """
    A question type that accepts text input.
    """
    question_set = models.ForeignKey(
        QuestionSet, related_name='text_questions')
    input_size = models.CharField(max_length=64, choices=[
        ('1', 'short answer: (1 row 50 cols)'),
        ('5', 'sentence: (5 rows 50 cols'),
        ('15', 'paragraph(s): (15 rows 50 cols)')], default='1')
    correct = models.TextField(blank=True)
    responses = GenericRelation('QuestionResponse')
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)

    def get_question_type(self):
        return 'text'

    def get_input_widget(self):
        widget_attrs = {
            'rows': self.input_size,
            'cols': 40,
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
            return self.responses.get(user=user)
        except:
            return None

    def get_edit_url(self, course):
        return reverse('text_question_update', args=[course.slug, self.id])

    def get_absolute_url(self):
        return reverse('text_question', args=[self.id])


class OptionQuestion(AbstractQuestion):

    """
    A question type that accepts a selection from a list of choices (multiple choice).
    """
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')

    question_set = models.ForeignKey(
        QuestionSet, related_name='option_questions')
    responses = GenericRelation('QuestionResponse')
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)

    def get_question_type(self):
        return 'option'

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
            return [i.id for i in self.options.filter(correct=True)]
        else:
            return [i.id for i in self.options.filter(correct=True)]

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
            # optresponse = self.responses.get(user=user).response.replace('"','')
            # return Option.objects.get(pk=int(optresponse)).display_text
            return self.responses.get(user=user)

        except:
            return None

    def get_edit_url(self, course):
        return reverse('option_question_update', args=[course.slug, self.id])

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

    # Fix this to construct arguments relative to question sequence object
    def get_absolute_url(self):
        return reverse('home')


class UserWorksheetStatus(TimeStampedModel):
    """
    Maintains record of completed worksheets by user.
    """
    user = models.ForeignKey(User, related_name='completed_worksheets')
    completed_worksheet = models.ForeignKey(QuestionSet)
