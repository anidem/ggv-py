from django.db import models
from itertools import chain
from operator import attrgetter
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class LessonManager(models.Manager):
    # use_for_related_fields = True

    def activities(self, **kwargs):
        lesson_obj = Lesson.objects.get(pk=kwargs['id'])
        questions = lesson_obj.worksheets.all()
        slidestacks = lesson_obj.slidestacks.all()
        activity_set = list(chain(questions, slidestacks))
        activity_set = sorted(activity_set, key=attrgetter('section.display_order','display_order'))
        return activity_set

class Lesson(models.Model):
    MATH = 'MATH'
    SPMATH = 'SP_MATH'
    SCIENCE = 'SCI'
    SPSCIENCE = 'SP_SCI'
    SOCSTUDIES = 'SOCSTUDIES'
    SPSOCSTUDIES = 'SP_SOCSTUDIES'
    WRITING = 'WRITING'
    SPWRITING = 'SP_WRITING'

    LESSON_SUBJECTS = (
        (MATH, 'Math'),
        (SPMATH, 'Math en Espanol'),
        (SCIENCE, 'Science'),
        (SPSCIENCE, 'Science en Espanol'),
        (SOCSTUDIES, 'Social Studies'),
        (SPSOCSTUDIES, 'Social Studies en Espanol'),
        (WRITING, 'Writing'),
        (SPWRITING, 'Writing en Espanol'),
    )

    title = models.CharField(max_length=256, default='Subject')
    subject = models.CharField(max_length=32, choices=LESSON_SUBJECTS)

    objects = LessonManager()    

    def check_membership(self, user):
        courses = self.course_set.all()
        for i in courses:
            if user.has_perm('view_course', i):
                return True
        return False

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.id)])

class Section(models.Model):
    title = models.CharField(max_length=256)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['title', 'display_order']

    def __unicode__(self):
        return self.title

class AbstractActivity(models.Model):
    title = models.CharField(max_length=256)
    section = models.ForeignKey(Section, null=True, blank=True)
    display_order = models.IntegerField()

    def check_membership(self, user):
        return self.lesson.check_membership(user)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['section', 'display_order']




