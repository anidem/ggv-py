# courses/models.py
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from itertools import chain
import operator

from guardian.shortcuts import get_users_with_perms, get_perms

from lessons.models import Lesson

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
    """
    Courses are synomous with a testing site. 
    A course contains one or more lessons and has zero or more designated instuctors and zero or more students.
    """
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=128, unique=True)
    access_code = models.CharField(max_length=8, null=True, blank=True)

    objects = ActivityReportManager()

    class Meta:
        permissions = (
            ('access', 'Access'),
            ('instructor', 'Instructor'),
            ('manage', 'Manager'),
        )

    def member_list(self):
        members = get_users_with_perms(self, attach_perms=True)
        return members

    def lesson_list(self):
        return self.crs_lessons.all()

    def get_user_role(self, user):
        return get_perms(user, self)

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.slug in user_session['user_courses']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', args=[str(self.slug)])

class CourseLesson(models.Model):
    """ 
        This class is used rather than a ManyToManyField in Course.
        Although it is nearly identical in function it is defined here to be more explicit
    """ 

    course = models.ForeignKey(Course, related_name='crs_lessons')
    lesson = models.ForeignKey(Lesson, related_name='crs_courses')

    def __unicode__(self):
        return '%s (%s)' % (self.course.title, self.lesson.title)

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.course.slug), str(self.lesson.id)])

class CoursePermission(models.Model):
    """
        This class maps users with courses. It also indicates the user role.
    """

    USER_ROLES = (
        ('manager', 'Manager'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )

    user = models.ForeignKey(User, related_name='user_course_permissions')
    course = models.ForeignKey(Course, related_name='course_permissions')
    role = models.CharField(max_length=48, choices=USER_ROLES, default='student')

    def __unicode__(self):
        return '%s %s (%s)' %(self.course, self.user, self.role)
