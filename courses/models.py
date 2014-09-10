from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from itertools import chain

from guardian.shortcuts import get_users_with_perms, get_perms

from lessons.models import Lesson

"""
Courses are synomous with a testing site. A course contains one or more lessons and has zero or more designated instuctors and zero or more students.
"""
class ActivityReportManager(models.Manager):
    def get_course_activity(self, **kwargs):
        try:
            user = kwargs.pop('user')
            time_range = kwargs.pop('time_range')
        except:
            return []

        worksheet_activity = []
        slide_activity = []

        activity = chain(worksheet_activity, slide_activity)

        return activity


class Course(models.Model):
    title = models.CharField(max_length=256)
    short_name = models.CharField(max_length=32)
    lessons = models.ManyToManyField(Lesson)
    access_code = models.CharField(max_length=8, null=True, blank=True)

    objects = ActivityReportManager()

    class Meta:
        permissions = (
            ('view_course', 'Course Access'),
            ('edit_course', 'Instructor'),
            ('manage_course', 'Manager'),
        )

    def member_list(self):
        return get_users_with_perms(self)

    def lesson_list(self):
        return self.lessons.all()

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.id in user_session['user_courses']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', args=[str(self.id)])
