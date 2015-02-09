# core/mixins.py
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import messages
from guardian.shortcuts import ObjectPermissionChecker

from courses.models import Course

class AccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """ 
        Successful execution of permission checks here rely on the object having a method
        check_membership being defined for the object. E.g. Course and Lesson each have this
        method.
        """
        try:
            if not self.get_object().check_membership(self.request.session):          
                self.template_name = 'access_error.html'
        except:
            self.template_name = 'access_error.html'        
        
        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)

class CourseContextMixin(object):
    
    def get_context_data(self, **kwargs):    
        """
        Intended to set context variable -- course -- based on request parameter crs_slug. Used in views to determine the course context for a request.
        """
        context = super(CourseContextMixin, self).get_context_data(**kwargs)
        try:
            context['course'] = Course.objects.get(slug=self.kwargs['crs_slug'])
        except Exception as e:
            print e
        return context
