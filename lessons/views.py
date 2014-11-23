# lessons/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin
from courses.models import Course, CourseLesson

from .models import Lesson
from .forms import StudentAccessForm


class LessonView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'

    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            course = self.object.crs_courses.get(course__slug=kwargs.pop('crs_slug'))
        except CourseLesson.DoesNotExist:
            self.template_name = 'access_error.html'
            return self.render_to_response([])

        # Adding course to the context data.
        context = self.get_context_data(object=self.object, course=course)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()
        context['acts'] = Lesson.objects.activities(id=lesson.id) # using custom model manager
        context['sections'] = lesson.sections.all()
        return context