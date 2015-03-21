# lessons/views.py
from django.views.generic import DetailView
from django.contrib.contenttypes.models import ContentType


from braces.views import LoginRequiredMixin

from core.mixins import CourseContextMixin, AccessRequiredMixin
from core.forms import BookmarkForm
from core.models import Bookmark
from .models import Lesson


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
                bookmark_label = bookmark.mark_type
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
