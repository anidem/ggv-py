# lessons/views.py
from django import forms
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy



from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from core.mixins import CourseContextMixin, AccessRequiredMixin
from core.models import Bookmark
from .models import Lesson, Section
from questions.models import Option


class LessonView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'
    access_object = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()

        activity_list = []
        bookmarks = Bookmark.objects.filter(creator=self.request.user).filter(course_context=context['course'])

        for i in lesson.activities():
            activity_type=ContentType.objects.get_for_model(i).id
            bookmark = None
            bookmark_label = ''
            bookmark_id = ''
            try:
                bookmark = bookmarks.filter(content_type=activity_type).get(object_id=i.id)
                bookmark_label = bookmark.get_mark_type_display()
                bookmark_id = bookmark.id
                # bookmarkform = BookmarkForm(instance=bookmark)

            except:
                pass
                # bookmark = None
                # initial_bookmark_data = {}
                # initial_bookmark_data['content_type'] = activity_type.id
                # initial_bookmark_data['object_id'] = i.id
                # initial_bookmark_data['creator'] = self.request.user
                # initial_bookmark_data['course_context'] = context['course']
                # bookmarkform = BookmarkForm(initial=initial_bookmark_data)

            a = {}
            a['act'] = i
            a['act_type_id'] = activity_type
            a['note'] = None
            # a['bookmarkform'] = bookmarkform
            a['bookmark'] = bookmark
            a['bookmark_id'] = bookmark_id
            a['bookmark_label'] = bookmark_label
            a['date'] = None

            activity_list.append(a)

        context['acts'] = activity_list
        context['sections'] = lesson.sections.all()
        context['is_staff'] = self.request.user.is_staff

        return context

class SectionUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, CourseContextMixin, UpdateView):
    model = Section
    template_name = 'activity_update.html'
    # form_class = QuestionSetUpdateForm

    def get_success_url(self):
        return reverse_lazy('lesson', args=[self.context['course'], self.get_object().lesson.id])

    def get_context_data(self, **kwargs):
        context = super(SectionUpdateView, self).get_context_data(**kwargs)
        return context

class WorksheetKeyView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = Lesson
    template_name = 'question_worksheet_key.html'

    def get_context_data(self, **kwargs):
        context = super(WorksheetKeyView, self).get_context_data(**kwargs)
        key = []
        worksheets = self.get_object().worksheets.all()
        for i in worksheets:
            k_items = []
            for question in i.get_ordered_question_list():
                try:
                    if(question.get_question_type() == 'option'):
                        answer = Option.objects.get(question.correct_answer()).display_text
                    else:
                        answer = question.correct_answer()
                    k_items.append((question.display_text, answer))
                except:
                    pass

            key.append((i, k_items))

        context['worksheets'] = key
        return context




