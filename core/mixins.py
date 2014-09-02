# core/mixins.py
from django.shortcuts import render, redirect

from django.contrib import messages
from guardian.shortcuts import ObjectPermissionChecker

class AccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        try:
            print self.get_object().check_membership(self.request.user)
            
            if not self.get_object().check_membership(self.request.user):          
                self.template_name = '404.html'

        except:
            self.template_name = '404.html'
        
        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)

