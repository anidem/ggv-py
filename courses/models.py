# courses/models.py

from operator import attrgetter

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from guardian.shortcuts import get_users_with_perms, get_perms

from lessons.models import Lesson

ws_control_choices = (
    (False, 'OPTION 1: Students have full access to continue in GGV. Students are allowed to review worksheet results, make corrections, and continue in GGV.'),
    (True, 'OPTION 2: Students have restricted access to continue in GGV. Students are not allowed to review worksheet results, make corrections, and continue in GGV without instructor permission. Instructor must follow the steps below for option 2. ')
)

class Course(models.Model):

    """
    Courses are synonymous with a testing site.
    A course contains one or more lessons and has zero or more designated instuctors and zero or more students.
    """
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=128, unique=True)
    control_worksheet_results = models.BooleanField(default=False, choices=ws_control_choices)
    access_code = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        permissions = (
            ('access', 'Access'),
            ('instructor', 'Instructor'),
            ('manage', 'Manager'),
        )

    def member_list(self):

        return get_users_with_perms(self, attach_perms=True)

    def student_list(self, extra_details=None, sort_by='first_name', reverse_sort=False):
        # if extra_details:
        # return [{user: ActivityLog.objects.filter(user=user)} for user, perms
        # in self.member_list().items() if 'access' in perms]

        students = [user for user, perms in self.member_list().items() if 'access' in perms and not user.is_staff and not user.is_superuser and 'instructor' not in perms]
        return sorted(students, key=attrgetter(sort_by), reverse=reverse_sort)

    def instructor_list(self):
        return [user for user, perms in self.member_list().items() if 'instructor' in perms]

    def manager_list(self):
        return [user for user, perms in self.member_list().items() if 'manage' in perms]

    def deactivated_list(self):
        return [user for user, perms in self.member_list().items() if not perms and user.social_auth.all()]

    def unvalidated_list(self):
        return [user for user, perms in self.member_list().items() if not perms and not user.social_auth.all()]

    def lesson_list(self):
        return self.crs_lessons.all()

    def get_user_role(self, user):
        return get_perms(user, self)

    def get_edit_privilege(self, user):
        return 'instructor' in self.get_user_role(user)

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
    role = models.CharField(
        max_length=48, choices=USER_ROLES, default='student')

    def __unicode__(self):
        return '%s %s (%s)' % (self.course, self.user, self.role)
