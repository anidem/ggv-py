from itertools import chain
from operator import attrgetter
import json, ast

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django import forms

from model_utils.models import TimeStampedModel

from lessons.models import Lesson, AbstractActivity, Section
from notes.models import UserNote
from core.models import Bookmark


class QuestionSet(AbstractActivity):
    lesson = models.ForeignKey(
        Lesson, null=True, blank=True, related_name='worksheets')
    activity_type = models.CharField(max_length=48, default='worksheet', null=True)
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)
    display_pdf = models.FileField(null=True, blank=True, upload_to='pdf')
    time_limit = models.PositiveIntegerField(default=0, blank=True, help_text="(Optional) # of minutes allowed to complete worksheet")
    pretest_subject = models.CharField(max_length=24, null=True, blank=True, help_text='Associate this worksheet to: math, science, socialstudies, writing. Only set this for worksheets that are used as pretests.')

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.lesson in user_session['user_lessons']

    def get_question_at_index(self, index):
        """
        Should return a dict with an index and question object indicated by index.
        Index is question order. E.g., index 0 is the first question in the worksheet.

        UNIT TEST ==> test_worksheet_question_listing()
        """
        try:
            question = self.get_ordered_question_list()[index]
            return {'index': index, 'question': question}
        except:
            return None

    def get_next_question(self, user):
        """
        Should return dict with an index and question object indicating the 
        relative index of the next unanswered question for user.

        NOTE: this is returning the logical ordering. E.g., first item begins ordering at 1.
        Will need to normalize this. The logical ordering is used for the request url?
        
        If this is the last question, None will be returned.
        
        UNIT TEST ==> test_worksheet_question_listing()
        """
        questions = self.get_ordered_question_list(required_questions=True)
        index = 1
        for i in questions:
            if not i.user_response_object(user):
                return {'index': index, 'question': i}
            index = index + 1
        return None

    def get_ordered_question_list(self, required_questions=False):
        """
        Should return a list of questions (text and option) in specified display order.
        
        If required_questions filter is True, only questions that require a response are returned.
        This particular case is used when scoring (we don't score a question that does not require a response).

        UNIT TEST ==> test_worksheet_question_listing()
        """
        if required_questions:
            option_questions = self.option_questions.filter(response_required=True)
            text_questions = self.text_questions.filter(response_required=True)
        else:
            option_questions = self.option_questions.all()
            text_questions = self.text_questions.all()
        
        questions = sorted(
            chain(option_questions, text_questions),
            key=attrgetter('display_order')
        )
        return questions

    def get_num_questions(self, required_questions=False):
        """
        Should return an integer indicating the number of questions assigned to this worksheet.

        If required_questions filter is True, the count reflects only those questions that require a response.

        UNIT TEST ==> test_worksheet_question_listing()
        """
        if required_questions:
            return self.option_questions.filter(response_required=True).count() + self.text_questions.filter(response_required=True).count()
        return self.option_questions.all().count() + self.text_questions.all().count()

    def get_prev_question(self, current):
        """
        Should return a question object ordered directly before index indicated current.
        Returns None if index out of range.

        UNIT TEST ==> test_worksheet_question_listing()
        """
        if current > 0:
            questions = self.get_ordered_question_list()
            return questions[current-1]
        return None

    def get_user_score(self, user):
        """
        Calculates and returns a score based on responses to this worksheet by user.
        Score is computed as a percentage (0.00 - 100.00). Null responses indicate that user
        has not submitted a response to that question.

        Uses get_ordered_question_list(required_questions=True) to only score responses for questions 
        that require a response.
        """
        responses = []
        for i in self.get_ordered_question_list(required_questions=True):
            responses.append(i.user_response_object(user))
        
        num_correct = 0
        for i in responses:
            if i and i.iscorrect:
                num_correct = num_correct + 1 
        try:
            return (float(num_correct)/len(responses))*100
        except:
            return None

    def get_user_response_objects(self, user):
        """
        Returns a list of QuestionResponse objects related to this worksheet and user.
        This list may contain None values where a response to a question has not been submitted OR 
        the question does not require a response.
        """
        responses = []
        for i in self.get_ordered_question_list():
            responses.append(i.user_response_object(user))

        return responses

    def get_pretest_user_response_objects(self, user):
        """
        Returns a dictionary containing:
        a) number of responses that are not null

        b) list of PretestQuestionResponse objects related to this worksheet and user.
        This list may contain None values where a response to a question has 
        not been submitted OR the question does not require a response.

        c) a compiled number of correct responses in (a).
        """
        responses = {'count': 0, 'responses': [], 'num_correct': 0}
        for i in self.get_ordered_question_list():
            resp = i.pretestuser_response_object(user)
            responses['responses'].append(resp)
            if i.response_required and resp:
                responses['count'] += 1
                if resp.iscorrect:
                    if resp.content_object.get_question_type() == 'text':
                        pass
                    responses['num_correct'] += 1

        return responses

    def get_user_responses(self, user, questions=None, course=None):

        report = []
        bookmarks = None
        bk = None

        if course:
            bookmarks = Bookmark.objects.filter(creator=user).filter(course_context=course)

        if not questions:
            questions = self.get_ordered_question_list()

        question_result = 0
        numcorrect = 0
        for i in questions:
            respobj = i.user_response_object(user)
            respstr = ''
            if respobj:
                question_type = respobj.content_object.get_question_type()
                resp = respobj.response
                if question_type == 'option':
                    if i.input_select == 'checkbox':
                        resplist = json.loads(resp)
                        for j in resplist:
                            respstr = respstr + ' (' + Option.objects.get(pk=j).display_text + ') '
                    else:
                        respstr = Option.objects.get(pk=resp).display_text

                elif question_type == 'text':
                    respstr = resp

                question_result = respobj.iscorrect
                if question_result:
                    numcorrect = numcorrect + 1

            elif not i.response_required:
                respstr = 'Response not required'

            else:
                respstr = 'Not answered'
                question_result = False
            
            question_type = ContentType.objects.get_for_model(i)
            if bookmarks:
                bookmark = bookmarks.filter(content_type=question_type.id).filter(object_id=i.id)
                if bookmark:
                    bk = bookmark[0]
                else:
                    bk = None          

            response = (bk, i, respstr, question_result, respobj)
            report.append(response)

        try:
            grade = UserWorksheetStatus.objects.filter(completed_worksheet=self).filter(user=user)[0].score
        except:
            grade = None

        return {'report': report, 'correct': numcorrect, 'numquestions': self.get_num_questions(required_questions=True), 'grade': grade}

    def get_all_responses(self, course):
        members = course.member_list()
        questions = self.get_ordered_question_list()
        report = []
        for i in members:
            user_report = self.get_user_responses(i, questions, course)
            responses = user_report['report']
            correct = user_report['correct']
            grade = user_report['grade']
            try:
                ws_status = UserWorksheetStatus.objects.filter(user=i).get(completed_worksheet=self.id)
            except:
                ws_status = None

            report.append((i, responses, correct, grade, ws_status))

        return report

    def delete_user_responses(self, user, course):
        questions = self.get_ordered_question_list()
        for i in questions:
            try:
                i.user_response_object(user).delete()
            except:
                pass
        status = user.completed_worksheets.filter(completed_worksheet=self).get() or None
        if status:
            status.delete()

    def notify_text(self, **kwargs):
        """ Expected kwargs: crs_slug, user associated with worksheet completion """
        target_url = self.get_absolute_url(crs_slug=kwargs['crs_slug'])
        text = '%s %s completed worksheet %s' % (kwargs['user'].first_name, kwargs['user'].last_name, target_url)
        
        return text

    def natural_key(self):
        return (self.lesson.title, self.title)

    def get_absolute_url(self, **kwargs):
        return reverse('worksheet_launch', args=[kwargs['crs_slug'], self.id])

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
    max_points = models.PositiveIntegerField(default=0)
    min_correct = models.PositiveIntegerField(default=1, help_text='Indicate minimum points to consider as correct.')
    content_area = models.ForeignKey(Section, models.SET_NULL, 
        null=True, blank=True, 
        help_text='(optional) Choose a related module (section) for this question.')
    extra_info = models.ForeignKey('ExtraInfo', models.SET_NULL, 
        null=True, blank=True, 
        help_text='(optional) Choose to add rubric and/or additional instructions')

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


class TextQuestion(AbstractQuestion):

    """
    A question type that accepts text input.
    """
    from pretests.models import PretestQuestionResponse

    question_set = models.ForeignKey(
        QuestionSet, related_name='text_questions')
    input_size = models.CharField(max_length=64, choices=[
        ('1', 'short answer: (1 row 50 cols)'),
        ('5', 'sentence: (5 rows 50 cols'),
        ('15', 'paragraph(s): (15 rows 50 cols)')], default='1')
    correct = models.TextField(blank=True)
    auto_grade = models.BooleanField(default=True, help_text='UNCHECK if this requires an external reader/grader')
    responses = GenericRelation('QuestionResponse')
    pretest_responses = GenericRelation(PretestQuestionResponse)
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)

    def get_question_type(self):
        return 'text'

    def get_django_content_type(self):
        return ContentType.objects.get_for_model(self)

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

    def check_answer_json(self, json_str):
        return json_str == self.correct

    def check_answer(self, question_response):
        if self.correct:  # Check if question has a correct answer specified.
            return question_response.response == self.correct
        if not self.auto_grade:  # checking if text question requires external grader.[1022, 1023, 1024, 1025]
            if question_response.score < self.min_correct:
                return False  # response needs to be graded or has been graded and is 0 (incorrect).
            return True  # score indicates that it is graded > 0 so is correct        
        return True

    def user_response_object(self, user):
        """
        Returns a QuestionResponse object related to user.
        """
        try:
            return self.responses.get(user=user)
        except:
            return None

    def pretestuser_response_object(self, user):
        """
        Returns a PretestQuestionResponse object related to user.
        """
        try:
            return self.pretest_responses.get(pretestuser=user)
        except:
            return None

    def get_edit_url(self, course):
        return reverse('text_question_update', args=[course.slug, self.id])

    def natural_key(self):
        return (self.question_set.title, self.display_text, self.display_order)

    def get_absolute_url(self):
        return reverse('text_question', args=[self.id])


class OptionQuestion(AbstractQuestion):

    """
    A question type that accepts a selection from a list of choices (multiple choice).
    """
    from pretests.models import PretestQuestionResponse
    
    input_select = models.CharField(max_length=64, choices=[(
        'radio', 'single responses'), ('checkbox', 'multiple responses')], default='radio')

    question_set = models.ForeignKey(
        QuestionSet, related_name='option_questions')
    responses = GenericRelation('QuestionResponse')
    pretest_responses = GenericRelation(PretestQuestionResponse)
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)

    
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
        return [(i.id, i.display_text) for i in self.options.all()]

    def correct_answer(self):
        return [i.id for i in self.options.filter(correct=True)]

    def check_answer_json(self, json_str):
        """
        Need to process option responses as lists. json used to coerce string representation to list.        
        """        
        try:
            return self.correct_answer() == json_str
        except:
            pass

    def check_answer(self, question_response):
        correct_ans_listing = self.correct_answer()
        
        if correct_ans_listing:   # Check if question has a correct answer specified.
            
            if self.input_select == 'checkbox':  # compare lists if question has multiple selections
                responsedata = question_response.json_response()
                response_listing = [int(i) for i in responsedata]
                return response_listing == correct_ans_listing

            # Implies a single selection option.
            return int(question_response.response) in correct_ans_listing

        return True  # If correct answer not specified return True

    def user_response_object(self, user):
        """
        Returns a QuestionResponse object related to user.
        """
        try:
            return self.responses.get(user=user)

        except:
            return None

    def pretestuser_response_object(self, user):
        """
        Returns a PretestQuestionResponse object related to user.
        """
        try:
            return self.pretest_responses.get(pretestuser=user)
        except:
            return None

    def get_edit_url(self, course):
        return reverse('option_question_update', args=[course.slug, self.id])

    def natural_key(self):
        return (self.question_set.title, self.display_text, self.display_order)

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
    iscorrect = models.BooleanField(blank=True, default=True)
    score = models.IntegerField(default=0)
    feedback = models.TextField(blank=True, default='')
    grade_request_sent = models.BooleanField(default=False)

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
            
        self.iscorrect = self.content_object.check_answer(self)
            
        super(QuestionResponse, self).save(*args, **kwargs)

        try:
            status = UserWorksheetStatus.objects.filter(completed_worksheet=self.content_object.question_set).get(user=self.user)
            status.update_score()
        
        except Exception as e:
            pass  # status object null, user has not completed all questions.

        

    # Fix this to construct arguments relative to question sequence object
    def get_absolute_url(self):
        return reverse('home')

    # class Meta:
    #     unique_together = (("user", "object_id", "content_type"),)


class UserWorksheetStatus(TimeStampedModel):
    """
    Maintains record of completed worksheets by user.
    Additionally, this object maintains whether a user can view their
    results. This property is checked if instructor as indicated they
    want to control/filter access to worksheet results.
    A completed worksheet also indicates a score (for fast retrieval in reporting)
    """
    user = models.ForeignKey(User, related_name='completed_worksheets')
    completed_worksheet = models.ForeignKey(QuestionSet)
    can_check_results = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def update_score(self):
        self.score = self.completed_worksheet.get_user_score(self.user)
        self.save()


class ExtraInfo(models.Model):
    """Stores extra information about a question.
    rubric: A rubric may be used to inform users on how an answer is 
    graded. E.g., how essay questions are graded.
    
    extra_instructions: Additional information and guidance on how to
    answer a question.
    """
    short_description = models.CharField(max_length=255, unique=True)
    rubric = models.TextField(null=True, blank=True)
    extra_instructions = models.TextField(null=True, blank=True)
    extra_help = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.short_description





