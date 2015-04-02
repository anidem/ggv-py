# core/signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from guardian.shortcuts import get_objects_for_user

from courses.models import Course
from .models import ActivityLog


@receiver(user_logged_in)
def init_session(sender, **kwargs):
    """
    This method is executed when a user logs in. It initializes two session variables:
    user_courses: a list of course slugs of which the logged in user has permissions
    user_lessons: a list of lessons assigned to courses
    """
    try:
        request = kwargs['request']
        user = kwargs['user']
        rem_addr = request.META['REMOTE_ADDR']

        course_permissions = get_objects_for_user(
            user, ['access', 'instructor', 'manage'], Course, any_perm=True)
        lesson_permissions = set()
        for i in course_permissions:
            for j in i.lesson_list():
                lesson_permissions.add(j.lesson.id)

        request.session['user_courses'] = [i.slug for i in course_permissions]
        request.session['user_lessons'] = list(lesson_permissions)

        ActivityLog(user=user, action='login', message=rem_addr).save()

    except Exception as e:
        print 'error in init session %s' % e


@receiver(user_logged_out)
def close_session(sender, **kwargs):
    """
    This method is executed when a user logs out.
    """
    try:
        user = kwargs['user']

        ActivityLog(
            user=user, action='logout', message='user logged out').save()

    except Exception as e:
        print 'error in logout signal %s' % e
