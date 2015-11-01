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
    ('remember', 'Review,Revisa'),
    ('todo', 'Need to Finish,Acabar'),
    ('started', 'Start,Comienza'),
    ('completed', 'Completed,Completado'),
    ('question', 'Question,Pregunta'),
    ('none', 'None,Borrar'),
)


class GGVUser(models.Model):
    user = models.OneToOneField(User)
    program_id = models.CharField(max_length=32, null=True, blank=True, unique=True)
    language_pref = models.CharField(max_length=32, default='english', choices=(
        ('english', 'english'), ('spanish', 'spanish')))
    clean_logout = models.BooleanField(default=True)
    receive_notify_email = models.BooleanField(default=False)
    receive_email_messages = models.BooleanField(default=False)

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

    def notify_text(self):

        if str(self.content_type) in ['option question', 'text question']:
            target_url = self.content_object.get_sequence_url(self.course_context)
        else:
            target_url = self.content_object.get_absolute_url(crs_slug=self.course_context.slug)

        text = '%s %s bookmarked (%s) %s' % (self.creator.first_name, self.creator.last_name, self.mark_type, target_url)
        return text

    def __unicode__(self):
        return self.mark_type

    class Meta:
        unique_together = ('mark_type', 'creator', 'content_type', 'object_id', 'course_context')


class Notification(models.Model):
    user_to_notify = models.ForeignKey(User)
    context = models.CharField(max_length=128)
    event = models.CharField(max_length=512, blank=True, null=True)
    logdata = models.ForeignKey(ActivityLog, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    def get_event_dict(self):
        return json.loads(self.event)

    def __unicode__(self):
        return '%s, %s' % (self.event, self.logdata)


class SiteMessage(models.Model):
    message = models.TextField(default='Message from ggvinteractive.com here.')
    url_context = models.CharField(max_length=512, default='/', unique=True)
    show = models.BooleanField(default=True)

    def __unicode__(self):
        return self.message


class SitePage(models.Model):
    title = models.TextField()
    content = models.TextField()

    def __unicode__(self):
        return self.title



