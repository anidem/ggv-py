from __future__ import unicode_literals
import json, ast
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from model_utils.models import TimeStampedModel
import pytz

from courses.models import GGVOrganization
from lessons.models import Lesson


def generate_token():
    import random
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    token = ''
    for i in range(8):
        token += random.choice(alpha)
    return token


class PretestAccount(models.Model):
    name = models.CharField(max_length=512)
    manager = models.ForeignKey(User, null=False, related_name='pretest_user_account')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    ggv_org = models.ForeignKey(GGVOrganization, null=True, blank=True)
    tokens_purchased = models.PositiveIntegerField(default=0)

    def pretest_user_list(self):
        """Returns a list of tuples (pretest user account object and number of exams they have started)
        """
        users = []
        for i in self.tokens.all():
            users.append((i, i.completion_status().count()))
        return users 
    
    def get_org_users(self):
        return self.ggv_org.licensed_user_list()

    def __unicode__(self):
        return self.name

class PretestUser(TimeStampedModel):
    """
    Models a non authenticated user who is granted access to a pretest worksheet.
    """
    account = models.ForeignKey(PretestAccount, related_name='tokens')
    access_token = models.CharField(max_length=512, unique=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=512, null=True, blank=True)
    last_name = models.CharField(max_length=512, null=True, blank=True)
    program_id = models.CharField(max_length=128, null=True, blank=True)    
    language_pref = models.CharField(max_length=32, null=True, blank=True, choices=(
        ('english', 'english'), ('spanish', 'spanish')))
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):        
        if not self.access_token:
            while True:
                self.access_token = generate_token()
                try:
                    super(PretestUser, self).save(*args, **kwargs)
                    break
                except:
                    pass
        else:
            super(PretestUser, self).save(*args, **kwargs)

    def completion_status(self):
        return self.pretest_user_completions.all()

    def pretest_bundle(self):
        """Returns the set of pretests the user is associated with.
        """
        attempts = self.pretest_user_completions.all()
        if attempts:
            return attempts[0].completed_pretest.lesson.activities()
        return []

    def __unicode__(self):
        return self.access_token

    class Meta:
        ordering = ['last_name', 'email']

class PretestUserCompletion(TimeStampedModel):
    """Stores when a user begins a worksheet. Instances of this class
    are created when a user begins a test. Because of this, records in this
    table are used to calculate expiration of tests and scores.
    """
    from questions.models import QuestionSet
    pretestuser = models.ForeignKey(PretestUser, related_name='pretest_user_completions')
    completed_pretest = models.ForeignKey(QuestionSet, related_name='pretest_completions')
    confirm_completed = models.BooleanField(default=False)

    def seconds_since_created(self):
        delta = datetime.now(pytz.utc) - self.created
        return delta.seconds

    def is_expired(self):
        if self.completed_pretest.time_limit < 1:
            return False
        return self.seconds_since_created() > (self.completed_pretest.time_limit * 60)

    def get_score(self):
        responses = self.completed_pretest.get_pretest_user_response_objects(self.pretestuser)
        score, ceiling = 0, 0
        for i in responses['responses']:
            if i and i.iscorrect:
                score += 8
            ceiling += 8
        return score, ceiling

    class Meta:
        unique_together = ('pretestuser', 'completed_pretest')

class PretestUserAssignment(models.Model):
    """2017-03-02 This is not in use as of yet."""
    pretestuser = models.ForeignKey(PretestUser, related_name='pretest_assignments')
    lesson = models.ForeignKey(Lesson, related_name='pretest_lessons')


class PretestQuestionResponse(TimeStampedModel):
    """
    Generic question response container for pretest worksheets.
    Designed to reference objects derived from questions.models.AbstractQuestion 
    (e.g., OptionQuestion, TextQuestion)

    A similar model is defined in questions.QuestionResponse
    """
    pretestuser = models.ForeignKey(PretestUser, related_name='pretest_responses')
    response = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    iscorrect = models.BooleanField(blank=True, default=True)

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
            
        super(PretestQuestionResponse, self).save(*args, **kwargs)   

    # Fix this to construct arguments relative to question sequence object
    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        unique_together = (("pretestuser", "object_id", "content_type"),)

