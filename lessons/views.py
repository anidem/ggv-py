# lessons/views.py
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import CourseContextMixin, AccessRequiredMixin
from core.forms import BookmarkForm
from courses.models import Course, CourseLesson
from notes.models import UserNote
from notes.forms import UserNoteForm

from .models import Lesson
from .forms import StudentAccessForm


class LessonView(LoginRequiredMixin, AccessRequiredMixin, CourseContextMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'
    access_object = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()

        acts = []

        for i in Lesson.objects.activities(id=lesson.id):
            try:
                bookmark = i.bookmarks.filter(creator=self.request.user).filter(course_context=context['course']).get()
                bookmarkform = BookmarkForm(instance=bookmark)

            except:
                bookmark = None
                initial_bookmark_data = {}
                initial_bookmark_data['content_type'] = ContentType.objects.get_for_model(i).id
                initial_bookmark_data['object_id'] = i.id
                initial_bookmark_data['creator'] = self.request.user
                initial_bookmark_data['course_context'] = context['course']                
                bookmarkform = BookmarkForm(initial=initial_bookmark_data)

            a = {}
            a['act'] = i
            a['note'] = None
            a['bookmarkform'] = bookmarkform
            a['bookmark'] = bookmark
            a['date'] = None

            acts.append(a)


        context['acts'] = acts 
        context['sections'] = lesson.sections.all()
        return context