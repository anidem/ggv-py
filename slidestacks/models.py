from django.db import models
from django.core.urlresolvers import reverse

from lessons.models import Lesson, AbstractActivity

class SlideStack(AbstractActivity):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, related_name='slidestacks')
    activity_type = models.CharField(max_length=48, default='slidestack')
    asset = models.CharField(max_length=512, default='not specified', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('slidestack', args=[str(self.id)])
