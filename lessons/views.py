# lessons/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, CourseContextMixin
from core.forms import BookmarkForm
from courses.models import Course, CourseLesson
from notes.models import UserNote
from notes.forms import UserNoteForm

from .models import Lesson
from .forms import StudentAccessForm


class LessonView(LoginRequiredMixin, AccessRequiredMixin, CourseContextMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()

        try:
            course = lesson.crs_courses.get(course__slug=self.kwargs.pop('crs_slug'))
        except CourseLesson.DoesNotExist:
            self.template_name = 'access_error.html'
            return self.render_to_response([])

        acts = []

        for i in Lesson.objects.activities(id=lesson.id):
            initial_bookmark_data = {}
            initial_bookmark_data['content_type'] = ContentType.objects.get_for_model(i).id
            initial_bookmark_data['object_id'] = i.id
            initial_bookmark_data['creator'] = self.request.user
            initial_bookmark_data['course_context'] = context['course'] 
            
            a = {}
            a['act'] = i
            a['note'] = None
            a['bookmarkform'] = BookmarkForm(initial=initial_bookmark_data)
            a['bookmark'] = i.bookmarks.filter(creator=self.request.user).filter(course_context=context['course'])
            a['date'] = None

            acts.append(a)


        context['acts'] = acts # using custom model manager 
        context['sections'] = lesson.sections.all()
        context['course'] = course
        return context