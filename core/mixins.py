# core/mixins.py
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from django.contrib import messages
from guardian.shortcuts import ObjectPermissionChecker

from courses.models import Course, CoursePermission

class AccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """ 
        Permission checks here rely on session variables user_courses and user_lessons
        to make checks without hitting database.
        """
        course_access = self.kwargs['crs_slug'] in self.request.session['user_courses']
        if not course_access:
            raise PermissionDenied  # early exit -- user accessing non assigned course      

        if self.access_object == 'lesson':
            course_access = self.get_object().id in self.request.session['user_lessons']
        elif self.access_object == 'activity':
            course_access = self.lesson.id in self.request.session['user_lessons']

        if not course_access:
            raise PermissionDenied         

        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)


class CourseContextMixin(object):

    def get_context_data(self, **kwargs):
        """
        Intended to set context variable -- course -- based on request parameter crs_slug. 
        Used in views to determine the course context for a request.
        """
        context = super(CourseContextMixin, self).get_context_data(**kwargs)
        try:
            context['course'] = Course.objects.get(
                slug=self.kwargs['crs_slug'])
        except Exception as e:
            print e

        return context
