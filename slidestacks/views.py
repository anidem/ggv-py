# slidestacks/views.py
import os, json
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView, RedirectView
from django.conf import settings

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from sendfile import sendfile

from core.mixins import AccessRequiredMixin
from core.models import ActivityLog
from .models import SlideStack



class SlideView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):

        slideroot = kwargs.pop('slideroot')
        slide = SlideStack.objects.get(pk=slideroot)
        
        abs_filename = os.path.join(
            os.path.join(settings.STACKS_ROOT, slide.asset),
            'html5.html'
        )

        ActivityLog(user=self.request.user, action='access', message=slideroot).save()
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
