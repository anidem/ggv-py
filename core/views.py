# core/views.py
from django.core.urlresolvers import reverse
from django.views.generic import View, TemplateView, CreateView, ListView, UpdateView

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user

from courses.models import Course

from .models import Bookmark
from .forms import BookmarkForm, PresetBookmarkForm
from .mixins import CourseContextMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggvhome.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = get_objects_for_user(
            self.request.user, 'view_course', Course)
        return context

class ActivityLogView(TemplateView):
    pass

class BookmarkAjaxCreateView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Bookmark

    def post_ajax(self, request, *args, **kwargs):
        bookmarkform = BookmarkForm(request.POST)
        if bookmarkform.is_valid():
            new_bookmark = bookmarkform.save()
            data = {}
            data['mark_type'] = new_bookmark.mark_type
            data['bookmark_id'] = new_bookmark.id
            return self.render_json_response(data)
        else:
            data = bookmarkform.errors
            return self.render_json_response(data)

class BookmarkAjaxUpdateView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, UpdateView):
    model = Bookmark

    def post_ajax(self, request, *args, **kwargs):
        bookmarkform = BookmarkForm(request.POST)
        if bookmarkform.is_valid():
            updated_bk = self.get_object()
            updated_bk.mark_type = bookmarkform.cleaned_data['mark_type']
            updated_bk.save()
            
            data = {}
            data['mark_type'] = updated_bk.mark_type
            data['bookmark_id'] = updated_bk.id
            return self.render_json_response(data)
        else:
            data = bookmarkform.errors
            return self.render_json_response(data)


class BookmarkAjaxDeleteView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, UpdateView):
    model = Bookmark

    def post_ajax(self, request, *args, **kwargs):
        bookmarkform = BookmarkForm(request.POST)
        if bookmarkform.is_valid():
            self.get_object().delete()
            data = {}
            data['deleted'] = 'deleted'
            return self.render_json_response(data)
        else:
            data = bookmarkform.errors
            return self.render_json_response(data)





