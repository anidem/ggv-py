from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.decorators import method_decorator

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin
from core.models import Course

from .models import Lesson, Activity
from .forms import StudentAccessForm


class LessonView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    """
    Display an individual :model:`myapp.MyModel`.

    **Context**

    ``RequestContext``

    ``mymodel``
        An instance of :model:`myapp.MyModel`.

    **Template:**

    :template:`myapp/my_template.html`

    """
    model = Lesson
    template_name = 'lesson.html'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()
        context['acts'] = lesson.activity_set.all()
        return context


class ActivityView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = Activity
    template_name = 'activity.html'



class StudentLessonView(AccessCodeRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'

    def get_context_data(self, **kwargs):
        context = super(StudentLessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()
        context['acts'] = lesson.activity_set.all()

        # REMOVE THIS AFTER TESTING
        del self.request.session['student_visitor']
        return context

class StudentActivityView(AccessCodeRequiredMixin, DetailView):
    model = Activity
    template_name = 'activity.html' 

class StudentAccessView(FormView):
    template_name = 'student_login.html'
    form_class = StudentAccessForm

    def form_valid(self, form):
        course = get_object_or_404(Course, access_code=form.cleaned_data['access_code'])
        if not course:
            return course
        self.success_url = '/ggvstudent/' + str(course.id)
        self.request.session['student_visitor'] = True
        return super(StudentAccessView, self).form_valid(form)