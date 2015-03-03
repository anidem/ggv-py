from django.db import models
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Lesson(models.Model):
    LESSON_SUBJECTS = (
        ('math', 'math'),
        ('science', 'science'),
        ('socialstudies', 'socialstudies'),
        ('writing', 'writing'),
        ('default', 'default'),
    )

    title = models.CharField(max_length=256, default='Subject')
    subject = models.CharField(max_length=32, choices=LESSON_SUBJECTS)
    language = models.CharField(max_length=32, default='eng', choices=(('eng', 'English'), ('span', 'Spanish')))
    icon_class = models.CharField(max_length=32, default='university', blank=True)

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.id in user_session['user_lessons']

    def activities(self):
        questions = self.worksheets.all()
        slidestacks = self.slidestacks.all()

        activity_set = list(
            chain(questions.filter(section__isnull=False), slidestacks.filter(section__isnull=False)))

        activity_set = sorted(
            activity_set, key=attrgetter('section.display_order', 'display_order'))
        orphans = list(chain(questions.filter(section__isnull=True),
                       slidestacks.filter(section__isnull=True)))
        activity_set += sorted(orphans, key=attrgetter('display_order'))

        return activity_set        

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.id)])


class Section(models.Model):
    title = models.CharField(max_length=256)
    display_order = models.IntegerField(default=0)
    lesson = models.ForeignKey(Lesson, related_name='sections')

    class Meta:
        ordering = ['lesson', 'display_order', 'title']

    def __unicode__(self):
        return self.title


class AbstractActivity(models.Model):
    title = models.CharField(max_length=256)
    instructions = models.TextField(null=True)
    section = models.ForeignKey(Section, null=True, blank=True)
    display_order = models.IntegerField()

    def check_membership(self, user_session):
        """ Delegates to its parent lesson container. """
        return self.lesson.check_membership(user_session)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['section', 'display_order']
