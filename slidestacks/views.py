# slidestacks/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView
import json

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from unipath import Path

from core.mixins import AccessRequiredMixin
from ggvproject.settings import base

from .models import SlideStack

class SlideStackView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = SlideStack
    template_name = 'slidestack_carousel.html'

    def get_context_data(self, **kwargs):
        context = super(SlideStackView, self).get_context_data(**kwargs) 
        # path = Path(base.PROJECT_DIR.child('static', 'stacks'), self.get_object().asset)
        # image_names = path.listdir(names_only=True)
        # context['slide_images'] = json.dumps(image_names)
        return context