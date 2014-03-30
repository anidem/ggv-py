# slidestacks/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin
from .models import SlideStack

class SlideStackView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = SlideStack
    template_name = 'act_slidestack.html'