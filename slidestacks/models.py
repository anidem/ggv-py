from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.fields import GenericRelation

from lessons.models import Lesson, AbstractActivity
from notes.models import UserNote
from core.models import Bookmark


class SlideStack(AbstractActivity):
    lesson = models.ForeignKey(
        Lesson, null=True, blank=True, related_name='slidestacks')
    activity_type = models.CharField(
        max_length=48, default='slidestack', null=True)
    asset = models.CharField(
        max_length=512, default='not specified', null=True, blank=True)
    notes = generic.GenericRelation(UserNote)
    bookmarks = GenericRelation(Bookmark)

    def get_absolute_url(self):
        return reverse('slideview', args=[str(self.asset)])
