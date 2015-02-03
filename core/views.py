# core/views.py
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, ListView

from braces.views import LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user

from courses.models import Course

class IndexView(TemplateView):
    template_name = 'index.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggvhome.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = get_objects_for_user(
            self.request.user, 'view_course', Course)
        return context

class ActivityLogView(TemplateView):
    pass





