# core/signals.py
from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone


from guardian.shortcuts import get_objects_for_user

from courses.models import Course
from .models import ActivityLog

@receiver(user_logged_in)
def init_session(sender, **kwargs):
    """
    This method is executed when a user logs in. It initializes two session variables:
    user_course: a list of course ids of which user has permissions to VIEW
    user_lessons: a list of lesson ids derived from the user_course list
    """
    try:
        request = kwargs['request']


        user = kwargs['user']
        rem_addr = request.META['REMOTE_ADDR']

        course_set = set()
        lesson_set = set()

        courses = get_objects_for_user(user, 'view_course', Course)
        for i in courses:
            course_set.add(i.id)
            for j in i.lesson_list():
                lesson_set.add(j.lesson.id)

        request.session['user_courses'] = list(course_set)
        request.session['user_lessons'] = list(lesson_set)

        ActivityLog(user=user, action='login', message=rem_addr).save()

    except Exception as e:
        print 'error in init session %s'% e

@receiver(user_logged_out)
def close_session(sender, **kwargs):
    """
    This method is executed when a user logs out.
    """
    try:
        user = kwargs['user']
        ActivityLog(user=user, action='logout', message='user logged out').save()

    except Exception as e:
        print 'error in logout signal %s'% e




