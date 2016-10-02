from django.db import models
from django.core.urlresolvers import reverse
# from django.contrib.contenttypes import generic
from django.contrib.contenttypes.fields import GenericRelation

from lessons.models import Lesson, AbstractActivity
from notes.models import UserNote
from core.models import Bookmark


class ExternalMedia(AbstractActivity):
    lesson = models.ForeignKey(
        Lesson, null=True, blank=True, related_name='external_media')
    activity_type = models.CharField(
        max_length=48, default='external_media', null=True)
    media_link = models.URLField(null=True, blank=True, help_text='copy and paste the link to the video. If you want to embed the video, please use the media embed field instead.')
    media_embed = models.TextField(null=True, blank=True, help_text='copy and paste the embed code from video service (e.g. from YouTube)')
    notes = GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)

    def __unicode__(self):
        return self.media_link

    def get_absolute_url(self, **kwargs):
        return reverse('external_media_view', args=[self.id])
