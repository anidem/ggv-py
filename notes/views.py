from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin

from .models import UserNote
from .forms import UserNoteForm

class NoteView(LoginRequiredMixin, ListView):
    model = UserNote
    template_name = 'note.html'

class NoteCreateView(LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = UserNote
    template_name = 'create_note.html'
    form_class= UserNoteForm
    # success_url = reverse_lazy('view_note')

    def post_ajax(self, request, *args, **kwargs):
        noteform = UserNoteForm(request.POST)
        if noteform.is_valid():
            newnote = noteform.save()
            data = {}
            data['modified'] = newnote.modified
            data['text'] = newnote.text
            data['creator'] = newnote.creator.username

            # print self.render_json_response(data)
            return self.render_json_response(data)
        else:
            data = noteform.errors
            print 'Errors?' , data
            return self.render_json_response(data)

