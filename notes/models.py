from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes import generic
from django.contrib.contenttypes.fields import GenericForeignKey

from model_utils.models import TimeStampedModel
from courses.models import Course


class UserNote(TimeStampedModel):
    text = models.TextField()
    creator = models.ForeignKey(User, related_name="user")
    content_type = models.ForeignKey(ContentType, related_name="content")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    course_context = models.ForeignKey(Course, null=True, blank=True)

    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('view_note', args=[str(self.id)])
