# slidestacks/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView
import json

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from unipath import Path

from core.mixins import AccessRequiredMixin
from ggvproject.settings import base

from .models import SlideStack

class SlideStackInitView(DetailView):
    model = SlideStack
    template_name = 'stack_init.html'

class SlideStackView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = SlideStack
    template_name = 'stack.html'

