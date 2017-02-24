from __future__ import unicode_literals
import json, ast

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from model_utils.models import TimeStampedModel

from courses.models import GGVOrganization
from lessons.models import Lesson
# from questions.models import TextQuestion, OptionQuestion, Option 

class PretestAccount(models.Model):
    name = models.CharField(max_length=512)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    ggv_org = models.ForeignKey(GGVOrganization, null=True, blank=True)

    def __unicode__(self):
        return self.name

class PretestUser(TimeStampedModel):
    """
    Models a non authenticated user who is granted access to a pretest worksheet.
    """
    account = models.ForeignKey(PretestAccount, related_name='tokens')
    access_token = models.CharField(max_length=512)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=512, null=True, blank=True)
    last_name = models.CharField(max_length=512, null=True, blank=True)
    program_id = models.CharField(max_length=128, null=True, blank=True)    
    language_pref = models.CharField(max_length=32, null=True, blank=True, choices=(
        ('english', 'english'), ('spanish', 'spanish')))
    expired = models.BooleanField(default=False)

    def __unicode__(self):
        return self.access_token


class PretestUserAssignment(models.Model):
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
