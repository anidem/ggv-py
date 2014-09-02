from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from model_utils.models import TimeStampedModel


class UserNote(TimeStampedModel):
    text = models.TextField()
    creator = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.text

    # def get_absolute_url(self):
    #     return reverse('course', args=[str(self.id)])