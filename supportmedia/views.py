from django.shortcuts import render
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
    model = ExternalMediaView
    lesson = None
    access_object = 'activity'
    template_name = 'external_media_create.html'


class ExternalMediaUpdateView(LoginRequiredMixin, AccessRequiredMixin, UpdateView):
    model = ExternalMediaView
    lesson = None
    access_object = 'activity'
    template_name = 'external_media_update.html'
