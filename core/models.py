# core/models.py
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
)

BOOKMARK_TYPES = (
    ('remember', 'Remember'),
    ('todo', 'To do'),
    ('started', 'Started'),
    ('completed', 'Completed'),
    ('question', 'Question'),
    ('none', 'None'),
)

class GGVUser(models.Model):
    user = models.OneToOneField(User)
    language_pref = models.CharField(max_length=32, default='english', choices=(('english', 'english'),('spanish', 'spanish')))
    clean_logout = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username

class ActivityLog(models.Model):

    user = models.ForeignKey(User)
    action = models.CharField(max_length=32, choices=ACTIONS)
    message = models.CharField(max_length=64, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
            ordering = ['user', '-timestamp']


class Bookmark(models.Model):
    mark_type = models.CharField(
    max_length=32, choices=BOOKMARK_TYPES, default='marked')
    creator = models.ForeignKey(User, related_name="bookmarker")
    content_type = models.ForeignKey(ContentType, related_name="bookmarks")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    course_context = models.ForeignKey(Course, null=True, blank=True)

    def __unicode__(self):
        return self.mark_type



