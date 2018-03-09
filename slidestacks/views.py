# slidestacks/views.py
import os
from django.views.generic import DetailView, UpdateView, RedirectView, TemplateView, View
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from sendfile import sendfile

from core.mixins import AccessRequiredMixin, CourseContextMixin
from core.models import ActivityLog

from .models import SlideStack


class slide_view(LoginRequiredMixin, AccessRequiredMixin, CourseContextMixin, DetailView):

    """ IFrame version that requires unprotected access to slidestacks. """

    model = SlideStack
    template_name = 'slidestack_view.html'
    lesson = None
    access_object = 'activity'

    def dispatch(self, *args, **kwargs):
        self.slide = self.get_object()
        self.lesson = self.slide.lesson
        msg_detail = self.lesson.title
        msg = '<a href="%s">%s</a>' % (self.request.path, self.slide.title)
        
        try:
            ActivityLog(
                user=self.request.user, action='access-presentation', message=msg, message_detail=msg_detail).save()
        except:
            raise PermissionDenied  # return a forbidden response

        return super(slide_view, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(slide_view, self).get_context_data(**kwargs)
        activities = self.get_object().section.activities()
        context['course'] = self.course
        context['next_act'] = ''
        context['section'] = self.get_object().section
        context['stacks_url'] = settings.STACKS_URL
        
        for i in range(len(activities)):
            if activities[i].id == self.get_object().id:
                try:
                    context['next_act'] = activities[i+1]
                except:
                    pass  # next activity doesn't exist. proceed silently   
        
        return context


class SlideView(LoginRequiredMixin, AccessRequiredMixin, RedirectView):
    """ Experimental component that routes all file access for ispring stacks through 
    this view and subsequently the SlideAssetHandlerView. If successful we can protect the ispring
    data from unauthorized access by configuring web server directory permissions
    """
    slide = None
    lesson = None
    access_object = 'activity'

    def dispatch(self, *args, **kwargs):
        try:
            asset = kwargs.pop('asset')
            self.slide = SlideStack.objects.get(asset=asset)
            self.lesson = self.slide.lesson
        except Exception as e:
            pass

        return super(SlideView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.lesson.id not in self.request.session['user_lessons']:
            raise PermissionDenied  # return a forbidden response
            return request

        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, self.slide.asset), 'index.html')

        msg_detail = self.lesson.title
        msg = '<a href="%s">%s</a>' % (request.path, self.slide.title)

        ActivityLog(
                user=self.request.user, action='access-presentation', message=msg, message_detail=msg_detail).save()
        return sendfile(request, abs_filename)


class SlideAssetHandlerView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        asset = kwargs.pop('asset')
        file = kwargs.pop('file')
        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, asset),
            os.path.join(settings.STACKS_DATA_DIR, file)
        )
        return sendfile(request, abs_filename)


class SlideStackInfoView(LoginRequiredMixin, StaffuserRequiredMixin, DetailView):
    model = SlideStack
    template_name = 'slidestack_view.html'


class SlideStackUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    model = SlideStack
    template_name = 'activity_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('slide_info_view', args=[self.get_object().id])
