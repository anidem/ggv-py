# core/views.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user

from courses.models import Course

@receiver(user_logged_in)
def init_session(sender, **kwargs):
    """
    This method is executed when a user logs in. It initializes two session variables:
    user_course: a list of course ids of which user has permissions to VIEW
    user_lessons: a list of lesson ids derived from the user_course list
    """
    try:
        request = kwargs['request']
        user = kwargs['user']
        course_set = set()
        lesson_set = set()

        courses = get_objects_for_user(user, 'view_course', Course)
        for i in courses:
            course_set.add(i.id)
            for j in i.lesson_list():
                lesson_set.add(j.id)

        request.session['user_courses'] = list(course_set)
        request.session['user_lessons'] = list(lesson_set)

    except:
        print 'error in init session'% request

class IndexView(TemplateView):
    template_name = 'index.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggvhome.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = get_objects_for_user(
            self.request.user, 'view_course', Course)
        return context
