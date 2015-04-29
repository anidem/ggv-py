# core/models.py
import json

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from courses.models import Course

ACTIONS = (
    ('login', 'login'),
    ('logout', 'logout'),
    ('access-question-text', 'access text question'),
    ('access-question-option', 'access multiple choice'),
    ('access-presentation', 'access presentation'),
    ('access-worksheet', 'access worksheet'),
    ('completed-worksheet', 'completed worksheet'),
)

BOOKMARK_TYPES = (
    ('remember', 'Review'),
    ('todo', 'Need to Finish'),
    ('started', 'Start'),
    ('completed', 'Completed'),
    ('question', 'Question'),
    ('none', 'None'),
)


class GGVUser(models.Model):
    user = models.OneToOneField(User)
    language_pref = models.CharField(max_length=32, default='english', choices=(
        ('english', 'english'), ('spanish', 'spanish')))
    clean_logout = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username


class ActivityLog(models.Model):
    user = models.ForeignKey(User, related_name='activitylog')
    action = models.CharField(max_length=32, choices=ACTIONS)
    message = models.CharField(max_length=512, null=True, blank=True)
    message_detail = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.timestamp.strftime('%b %d, %Y %-I:%M %p')

    class Meta:
        ordering = ['user', '-timestamp']


class Bookmark(models.Model):
    mark_type = models.CharField(
        max_length=32, choices=BOOKMARK_TYPES, default='none')
    creator = models.ForeignKey(User, related_name="bookmarker")
    content_type = models.ForeignKey(ContentType, related_name="bookmarks")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    course_context = models.ForeignKey(Course, null=True, blank=True)

    def __unicode__(self):
        return self.mark_type


class Notification(models.Model):
    user_to_notify = models.ForeignKey(User)
    event = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    def get_event_dict(self):
        return json.loads(self.event)

    def __unicode__(self):
        return self.event
