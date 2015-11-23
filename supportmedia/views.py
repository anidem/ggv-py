from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView, RedirectView, TemplateView, View, CreateView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from core.mixins import AccessRequiredMixin
from core.models import ActivityLog

from .models import ExternalMedia


class ExternalMediaView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = ExternalMedia
    lesson = None
    access_object = 'activity'
    template_name = 'external_media.html'


class ExternalMediaCreateView(LoginRequiredMixin, AccessRequiredMixin, CreateView):
    model = ExternalMedia
    lesson = None
    access_object = 'activity'
    template_name = 'external_media_create.html'
    fields = ['title', 'instructions', 'lesson', 'media_link', 'media_embed']


class ExternalMediaUpdateView(LoginRequiredMixin, AccessRequiredMixin, UpdateView):
    model = ExternalMedia
    lesson = None
    access_object = 'activity'
    template_name = 'external_media_update.html'
    fields = ['title', 'instructions', 'lesson', 'media_link', 'media_embed']

    def get_success_url(self):
        course = self.kwargs['crs_slug']
        return reverse('external_media_view', args=[course, self.get_object().id])
