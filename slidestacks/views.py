# slidestacks/views.py
import os, json
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView, RedirectView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.conf import settings

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from sendfile import sendfile

from core.mixins import AccessRequiredMixin
from core.models import ActivityLog
from .models import SlideStack



class SlideView(LoginRequiredMixin, AccessRequiredMixin, RedirectView):
    slide = None
    lesson = None
    access_object = 'activity'

    def dispatch(self, *args, **kwargs):
        try:
            slideroot = kwargs.pop('slideroot')
            self.slide = SlideStack.objects.get(pk=slideroot)
            self.lesson = self.slide.lesson
        except Exception as e:
            print e
            pass        
        
        return super(SlideView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.lesson.id not in self.request.session['user_lessons']:
            print 'NO ACCESS!'
            raise PermissionDenied  # return a forbidden response   
            return request 
     
        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, self.slide.asset),
            'html5.html'
        )
        print abs_filename

        ActivityLog(user=self.request.user, action='access', message=self.slide.id).save()
        return sendfile(request, abs_filename)


class SlideAssetHandlerView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        asset = kwargs.pop('asset')
        slideroot = kwargs.pop('slideroot')
        slide = SlideStack.objects.get(pk=slideroot)
        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, slide.asset),
            os.path.join(settings.STACKS_DATA_DIR, asset)
        )

        return sendfile(request, abs_filename)
