from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView, RedirectView, TemplateView, View, CreateView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from core.mixins import AccessRequiredMixin, CourseContextMixin
from core.models import ActivityLog

from .models import ExternalMedia
from .forms import UpdateExternalMediaForm


class ExternalMediaView(LoginRequiredMixin, DetailView):
    """ This method is defined to handle get absolute class methods..."""
    model = ExternalMedia
    access_object = None
    template_name = 'external_media.html'


class ExternalMediaCourseView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, DetailView):
    model = ExternalMedia
    access_object = None
    template_name = 'external_media.html'


class ExternalMediaCreateView(LoginRequiredMixin, AccessRequiredMixin, CreateView):
    model = ExternalMedia
    lesson = None
    section = None
    access_object = 'activity'
    template_name = 'external_media_create.html'
    form_class = UpdateExternalMediaForm

    def get(self, request, *args, **kwargs):
        self.lesson = request.GET.get('l') or None
        self.section = request.GET.get('s') or None
        return super(ExternalMediaCreateView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = self.initial.copy()
        initial['lesson'] = self.lesson
        initial['section'] = self.section
        return initial


class ExternalMediaUpdateView(LoginRequiredMixin, AccessRequiredMixin, UpdateView):
    model = ExternalMedia
    lesson = None
    access_object = 'activity'
    template_name = 'external_media_update.html'
    form_class = UpdateExternalMediaForm

