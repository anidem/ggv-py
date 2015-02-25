# core/mixins.py
from django.shortcuts import render, redirect
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
        try:
            print 'Checking access: ', self.access_object
            if self.access_object == 'course':
                if self.get_object().slug not in self.request.session['user_courses']:
                    self.template_name = 'access_error.html'
            elif self.access_object == 'lesson':
                if self.get_object().id not in self.request.session['user_lessons']:
                    self.template_name = 'access_error.html'
            elif self.access_object == 'activity':
                print 'checking', self.lesson
                if self.lesson.id not in self.request.session['user_lessons']:
                    self.template_name = 'access_error.html'

        except Exception as e:
            print e
            self.template_name = 'access_error.html'

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
