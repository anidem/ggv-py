# core/mixins.py
from django.shortcuts import render, redirect

from django.contrib import messages


class AccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        try:
            self.get_object().check_membership(self.request.user)
            
        except:
            self.template_name = '404.html'

        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)


class AccessCodeRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        if not self.request.session.get('student_visitor'):
            messages.error(
                self.request, 'Sorry. You don\'t have access to this material.')
            return redirect('student_login')
        return super(AccessCodeRequiredMixin, self).dispatch(*args, **kwargs)
