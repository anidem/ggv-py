# questions/views.py
import os, json, sys
from collections import OrderedDict

from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView, RedirectView
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory
from django import forms
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.conf import settings
from django.utils.text import slugify

from braces.views import CsrfExemptMixin, LoginRequiredMixin
from filebrowser.sites import site
from filebrowser.base import FileListing
from sendfile import sendfile

from core.models import Bookmark
from core.mixins import AccessRequiredMixin, CourseContextMixin
from core.forms import PresetBookmarkForm
from notes.models import UserNote
from notes.forms import UserNoteForm

from .models import TextQuestion, OptionQuestion, QuestionResponse, QuestionSet, Option
from .forms import QuestionResponseForm, OptionQuestionUpdateForm, TextQuestionUpdateForm, OptionFormset

def filter_filelisting_images(item):
    # item is a FileObject
    try:
        return item.filetype == "Image"
    except:
        return False


class QuestionAssetHandlerView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        asset = kwargs.pop('asset')
        abs_filename = os.path.join(
            os.path.join(settings.PDF_ROOT, asset)
        )
        return sendfile(request, abs_filename)

class WorksheetHomeView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'question_worksheet.html'


class QuestionResponseView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, CreateView):
    model = QuestionResponse
    template_name = 'question_sequence.html'
    form_class = QuestionResponseForm
    sequence = None

    def get_success_url(self):
        next_item = int(self.kwargs['j']) + 1
        course = self.kwargs['crs_slug']
        return reverse_lazy('question_response', args=[course, self.sequence.id, next_item])

    def get_initial(self):
        self.sequence = get_object_or_404(QuestionSet, pk=self.kwargs['i'])
        sequence_items = self.sequence.get_ordered_question_list()
        print self.sequence
        if sequence_items:
            item = sequence_items[int(self.kwargs['j'])-1]
        else:
            return redirect('http://localhost:8000')

        self.initial['question'] = item
        self.initial['user'] = self.request.user

        return self.initial

    def get_context_data(self, **kwargs):
        context = super(QuestionResponseView, self).get_context_data(**kwargs)
        if not self.sequence.lesson.check_membership(self.request.session):
            self.template_name = 'access_error.html'
            return context

        current_question = self.initial['question']
        
        # Tally -- move this to object manager...
        tally = OrderedDict()
        for i in self.sequence.get_ordered_question_list():

            try:
                response = i.user_response_object(
                    self.request.user).json_response()
                if i.check_answer(response):
                    tally[i] = 'success'
                else:
                    tally[i] = 'danger'
            except:
                tally[i] = 'default'

            if current_question.id == i.id:
                tally[i] = tally[i] + ' current'

        if self.request.user.is_staff:
            context['edit_url'] = current_question.get_edit_url(context['course'])

        question_index = self.sequence.get_ordered_question_list().index(current_question)+1
        initial_note_data = {}
        initial_note_data['content_type'] = ContentType.objects.get_for_model(current_question).id
        initial_note_data['object_id'] = current_question.id
        initial_note_data['creator'] = self.request.user
        initial_note_data['course_context'] = context['course']

        try:
            bookmark = current_question.bookmarks.filter(creator=self.request.user).filter(course_context=context['course']).get()
            context['bookmarkform'] = PresetBookmarkForm(instance=bookmark)
            context['bookmark'] = bookmark
        except:
            bookmark = None
            initial_bookmark_data = {}
            initial_bookmark_data['mark_type'] = 'question'
            initial_bookmark_data['content_type'] = ContentType.objects.get_for_model(current_question).id
            initial_bookmark_data['object_id'] = current_question.id
            initial_bookmark_data['creator'] = self.request.user
            initial_bookmark_data['course_context'] = context['course']
            
            context['bookmarkform'] = PresetBookmarkForm(initial=initial_bookmark_data)
            context['bookmark'] = bookmark        
        
        context['noteform'] = UserNoteForm(initial=initial_note_data)
        context['note_list'] = current_question.notes.all().filter(course_context=context['course']).order_by('-created')
        context['question'] = current_question
        context['question_position'] = question_index
        if question_index-1 > 0: 
            context['previous_position'] = question_index-1
        if question_index+1 <= len(list(tally)): 
            context['next_position'] = question_index+1
        context['question_list'] = tally
        context['worksheet'] = self.sequence
        context['instructor'] = self.request.user.has_perm('courses.edit_course')
        
        return context


class TextQuestionView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = TextQuestion
    template_name = 'question_view.html'

    def get_context_data(self, **kwargs):
        context = super(TextQuestionView, self).get_context_data(**kwargs)
        context['edit_url'] = self.get_object().get_edit_url(context['course'])
        context['sequence_url'] = self.get_object().get_sequence_url(context['course'])
        return context

class TextQuestionUpdateView(LoginRequiredMixin, CourseContextMixin, UpdateView):
    model = TextQuestion
    template_name = 'question_update.html'
    form_class = TextQuestionUpdateForm

    def get_success_url(self):
        course = self.kwargs['crs_slug']
        return reverse_lazy('text_question', args=[course, self.get_object().id])

class OptionQuestionView(LoginRequiredMixin, CourseContextMixin, DetailView):
    model = OptionQuestion
    template_name = 'question_view.html'
    
    def get_context_data(self, **kwargs):
        context = super(OptionQuestionView, self).get_context_data(**kwargs)
        context['options'] = self.get_object().options_list()
        context['edit_url'] = self.get_object().get_edit_url(context['course'])
        context['sequence_url'] = self.get_object().get_sequence_url(context['course'])
        return context

class OptionQuestionUpdateView(LoginRequiredMixin, CourseContextMixin, UpdateView):
    model = OptionQuestion
    template_name = 'question_update.html'
    form_class = OptionQuestionUpdateForm

    def get_success_url(self):
        course = self.kwargs['crs_slug']
        return reverse_lazy('option_question', args=[course, self.get_object().id])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        optionsform = OptionFormset(self.request.POST, instance=self.get_object())   
        if form.is_valid() and optionsform.is_valid():
            return self.form_valid(form, optionsform)
        else:
            return self.form_invalid(form, optionsform)

    def form_valid(self, form, optionsform):
        optionsform.save()
        return super(OptionQuestionUpdateView, self).form_valid(form)

    def form_invalid(self, form, optionsform):
        return self.render_to_response(
            self.get_context_data(form=form, optionsform=optionsform))

    def get_context_data(self, **kwargs):
        context = super(OptionQuestionUpdateView, self).get_context_data(**kwargs)
        context['optionsform'] =  OptionFormset(instance=self.get_object())
        
        context['filelisting'] = FileListing('img', filter_func=filter_filelisting_images, sorting_by='date', sorting_order='desc').files_listing_filtered()
        

        return context
