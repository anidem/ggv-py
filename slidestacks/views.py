# slidestacks/views.py
import os, json
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView, RedirectView

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from sendfile import sendfile

from core.mixins import AccessRequiredMixin
from .models import SlideStack

from django.conf import settings


class SlideView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        slideroot = kwargs.pop('slideroot')
        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, slideroot),
            'html5.html'
        )
        return sendfile(request, abs_filename)


class SlideAssetHandlerView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        asset = kwargs.pop('asset')
        slideroot = kwargs.pop('slideroot')
        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, slideroot),
            os.path.join(settings.STACKS_DATA_DIR, asset)
        )
        return sendfile(request, abs_filename)
