# core/mixins.py
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import messages
from guardian.shortcuts import ObjectPermissionChecker

class AccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """ 
        Successful execution of permission checks here rely on the object having a method
        check_membership being defined for the object. E.g. Courses and Lessons each have this
        method.
        """
        try:
            if not self.get_object().check_membership(self.request.session):          
                self.template_name = 'access_error.html'
        except:
            self.template_name = 'access_error.html'        
        
        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)
        
