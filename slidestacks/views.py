# slidestacks/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
import json

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from unipath import Path

from core.mixins import AccessRequiredMixin
from ggvproject.settings import base

from .models import SlideStack

class SlideStackView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = SlideStack
<<<<<<< HEAD
    template_name = 'slidestack_supersize.html'
=======
    template_name = 'slidestack_supersizer.html'
>>>>>>> 80366b8e0a1088b22757a7c3fd93cc2b8c21a2f2

    def get_context_data(self, **kwargs):
        context = super(SlideStackView, self).get_context_data(**kwargs) 
        path = Path(base.PROJECT_DIR.child('static', 'stacks'), self.get_object().id)
        image_names = path.listdir(names_only=True)
        img_list = []
        for i in image_names:
            img_obj = {}
            img_obj['image'] = '/static/stacks/%s/%s' % (self.get_object().id, i)
            img_list.append(img_obj)

        json_images = json.dumps(img_list)
        print json_images
        paginator = Paginator(image_names, 1)
        stack = []
        for i in range(paginator.num_pages):
            stack.append(paginator.page(i+1))

        context['initial'] = paginator.page(1).object_list[0]
        context['stack'] = stack
<<<<<<< HEAD
        context['slide_images'] = image_names
        context['json_images'] = json_images
=======
        context['slide_images'] = json.dumps(image_names)
>>>>>>> 80366b8e0a1088b22757a7c3fd93cc2b8c21a2f2
        return context