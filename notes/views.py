# notes/views.py
import datetime
from django.views.generic import CreateView, ListView, UpdateView

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin

from core.mixins import CourseContextMixin
from .models import UserNote
from .forms import UserNoteForm


class NoteView(LoginRequiredMixin, ListView):
    model = UserNote
    template_name = 'note.html'


class NoteCreateView(LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = UserNote
    template_name = 'create_note.html'
    form_class = UserNoteForm

    def post_ajax(self, request, *args, **kwargs):
        noteform = UserNoteForm(request.POST)
        if noteform.is_valid():
            newnote = noteform.save()
            data = {}
            data['modified'] = newnote.modified.strftime("%b %d %Y %H")
            data['text'] = newnote.text
            data['creator'] = newnote.creator.username
            return self.render_json_response(data)
        else:
            data = noteform.errors
            return self.render_json_response(data)


class NoteDeleteView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, UpdateView):
    model = UserNote

    def post_ajax(self, request, *args, **kwargs):
        noteform = UserNoteForm(request.POST)
        if noteform.is_valid():
            self.get_object().delete()
            data = {}
            data['deleted'] = 'deleted'
            return self.render_json_response(data)
        else:
            data = noteform.errors
            return self.render_json_response(data)
