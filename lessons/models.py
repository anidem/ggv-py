from django.db import models
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse


class Lesson(models.Model):
    LESSON_SUBJECTS = (
        ('math', 'math'),
        ('science', 'science'),
        ('socialstudies', 'socialstudies'),
        ('writing', 'writing'),
        ('pre_math', 'pre_math'),
        ('pre_science', 'pre_science'),
        ('pre_socialstudies', 'pre_socialstudies'),
        ('pre_writing', 'pre_writing'),
        ('default', 'default'),
    )

    title = models.CharField(max_length=256, default='Subject')
    subject = models.CharField(max_length=32, choices=LESSON_SUBJECTS)
    language = models.CharField(
        max_length=32, default='eng', choices=(('eng', 'English'), ('span', 'Spanish')))
    icon_class = models.CharField(
        max_length=32, default='university', blank=True)

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.id in user_session['user_lessons']

    def activities(self):
        questions = self.worksheets.all()
        slidestacks = self.slidestacks.all()
        external_media = self.external_media.all()

        activity_set = list(chain(
            questions.filter(section__isnull=False),
            slidestacks.filter(section__isnull=False),
            external_media.filter(section__isnull=False)))
        activity_set = sorted(
            activity_set, key=attrgetter('section.display_order', 'display_order'))
        orphans = list(chain(questions.filter(section__isnull=True),
                             slidestacks.filter(section__isnull=True),
                             external_media.filter(section__isnull=True)))
        activity_set += sorted(orphans, key=attrgetter('display_order'))

        return activity_set

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.id)])


class Section(models.Model):
    title = models.CharField(max_length=256)
    subtitle = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    lesson = models.ForeignKey(Lesson, related_name='sections')

    def activities(self):
        questions = self.lesson.worksheets.filter(section=self)
        slidestacks = self.lesson.slidestacks.filter(section=self)
        external_media = self.lesson.external_media.filter(section=self)
        activity_set = list(chain(questions, slidestacks, external_media))
        activity_set = sorted(
            activity_set, key=attrgetter('section.display_order', 'display_order'))
        return activity_set

    class Meta:
        ordering = ['lesson', 'display_order', 'title']

    def __unicode__(self):
        return self.title


class AbstractActivity(models.Model):
    title = models.CharField(max_length=256)
    instructions = models.TextField(null=True, blank=True)
    section = models.ForeignKey(Section, models.SET_NULL, null=True, blank=True)
    display_order = models.IntegerField()

    def check_membership(self, user_session):
        """ Delegates to its parent lesson container. """
        return self.lesson.check_membership(user_session)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['section', 'display_order']
