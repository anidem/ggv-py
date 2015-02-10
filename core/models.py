# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


from courses.models import Course

ACTIONS = (
    ('login', 'login'),
    ('logout', 'logout'),
    ('access', 'access'),
)

BOOKMARK_TYPES = (
    ('remember', 'Remember'),
    ('todo', 'Todo'),
    ('started', 'Started'),
    ('completed', 'Completed'),
    ('question', 'Question'),
    ('none', 'None'),
)

class ActivityLog(models.Model):

    """
    Probably need to have a custom manager for this model.
    """
    user = models.ForeignKey(User)
    action = models.CharField(max_length=32, choices=ACTIONS)
    message = models.CharField(max_length=64, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Bookmark(models.Model):
    mark_type = models.CharField(max_length=32, choices=BOOKMARK_TYPES, default='marked')
    creator = models.ForeignKey(User, related_name="bookmarker")
    content_type = models.ForeignKey(ContentType, related_name="bookmarks")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    course_context = models.ForeignKey(Course, null=True, blank=True)
    
    def __unicode__(self):
        return self.mark_type






