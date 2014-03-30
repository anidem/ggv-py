# core/views.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user

from courses.models import Course

@receiver(user_logged_in)
def init_session(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']
    courses = get_objects_for_user(
        user, 'view_course', Course).values_list('id', flat=True)
    request.session['user_courses'] = []
    for i in courses:
        request.session['user_courses'].append(i)


class IndexView(TemplateView):
    template_name = 'index.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggv.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = get_objects_for_user(
            self.request.user, 'view_course', Course)
        return context
