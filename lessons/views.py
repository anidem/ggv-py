# lessons/views.py
from django import forms
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy



from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from core.mixins import CourseContextMixin, AccessRequiredMixin, PrivelegedAccessMixin
from core.models import Bookmark, BOOKMARK_TYPES
from core.utils import activity_stat_worksheet, activity_stat_slides
from .models import Lesson, Section
from questions.models import Option


class LessonView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'
    access_object = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        lesson = self.get_object()

        opts = dict(BOOKMARK_TYPES)
        print opts
        for i, j in opts.items():
            if self.request.user.ggvuser.language_pref == 'spanish':
                opts[i] = j.split(',')[1]
            else:
                opts[i] = j.split(',')[0]

        print opts
        context['bookmark_type_opts'] = opts

        activity_list = []
        bookmarks = Bookmark.objects.filter(creator=self.request.user).filter(course_context=context['course'])

        completions = self.request.user.completed_worksheets.all()
        for i in lesson.activities():
            activity_type = ContentType.objects.get_for_model(i).id
            bookmark = None
            bookmark_label = ''
            bookmark_id = ''
            bookmark_type = 'none'
            try:
                bookmark = bookmarks.filter(content_type=activity_type).get(object_id=i.id)

                label = bookmark.get_mark_type_display()
                # if lesson.language == 'span':
                if self.request.user.ggvuser.language_pref == 'spanish':
                    label = label.split(',')[1]
                else:
                    label = label.split(',')[0]

                bookmark_label = label
                bookmark_id = bookmark.id
                bookmark_type = bookmark.mark_type

                # bookmarkform = BookmarkForm(instance=bookmark)

            except:
                pass

            a = {}
            a['act'] = i
            a['act_type_id'] = activity_type
            a['note'] = None
            # a['bookmarkform'] = bookmarkform
            a['bookmark'] = bookmark
            a['bookmark_id'] = bookmark_id
            a['bookmark_label'] = bookmark_label
            a['bookmark_type'] = bookmark_type
            a['date'] = None
            if activity_type == 13:  # worksheet activity
                a['score'] = completions.filter(completed_worksheet=i)

            activity_list.append(a)

        #  build user activity stats info
        context['worksheets_stat'] = activity_stat_worksheet(self.request.user, lesson)
        context['slides_stat'] = activity_stat_slides(self.request.user, lesson)

        context['acts'] = activity_list
        context['sections'] = lesson.sections.all()
        context['is_staff'] = self.request.user.is_staff
        context['instructor'] = self.request.user in context['course'].instructor_list() or self.request.user.is_staff
        context['language_pref'] = self.request.user.ggvuser.language_pref

        return context

class SectionUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, CourseContextMixin, UpdateView):
    model = Section
    template_name = 'activity_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('lesson', args=[self.kwargs['crs_slug'], self.get_object().lesson.id])

    def get_context_data(self, **kwargs):
        context = super(SectionUpdateView, self).get_context_data(**kwargs)
        return context







