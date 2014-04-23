# lessons/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin

from .models import Lesson
from .forms import StudentAccessForm


class LessonView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()
        context['acts'] = Lesson.objects.activities(id=lesson.id) # using custom model manager
        return context


# TODO: Refactor the student views.
# class StudentLessonView(AccessCodeRequiredMixin, DetailView):
#     model = Lesson
#     template_name = 'lesson.html'

#     def get_context_data(self, **kwargs):
#         context = super(StudentLessonView, self).get_context_data(**kwargs)
#         lesson = self.get_object()
#         context['acts'] = lesson.activity_set.all()
#         return context


# class StudentActivityView(AccessCodeRequiredMixin, DetailView):
#     model = Activity
#     template_name = 'activity.html'


class StudentAccessView(FormView):
    template_name = 'student_login.html'
    form_class = StudentAccessForm

    def form_valid(self, form):
        course = get_object_or_404(
            Course, access_code=form.cleaned_data['access_code'])
        if not course:
            return course
        self.success_url = '/ggvstudent/' + str(course.id)
        self.request.session['student_visitor'] = True
        return super(StudentAccessView, self).form_valid(form)
