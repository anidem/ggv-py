# questions/views.py
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
import json

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin
from .models import QuestionSet, MultipleChoiceQuestion, ShortAnswerQuestion, QuestionResponse
from .forms import QuestionPostForm
from .mixins import AjaxableResponseMixin


class QuestionFormView(CreateView):
    model = QuestionResponse
    form_class = QuestionPostForm
    template_name = 'formtest.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionFormView, self).get_context_data(**kwargs)
        formset = modelformset_factory(QuestionResponse)
        context['form'] = formset
        return context


class QuestionSetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet.html'
    questions = []

    def post(self, request, *args, **kwargs):
        messages = []
        errors = []
        data = dict()
        ResponseFormset = formset_factory(QuestionPostForm)
        formset = ResponseFormset(request.POST)

        if formset.is_valid():
            for form in formset.cleaned_data:
                question = form['question_type'].get_object_for_this_type(
                    pk=form['question_id'])
                try:
                    # check for previous response
                    resp = question.responses.get(user=request.user)
                    if resp.response != form['response']:
                        resp.response = form['response']
                        resp.save()
                except:
                    resp = QuestionResponse()
                    resp.user = request.user
                    resp.response = form['response'] or None
                    resp.question_type = form['question_type']
                    resp.question_id = question.id
                    resp.content_object = question
                    resp.save()

        data['messages'] = messages
        # data = json.dumps(self.get_context_data(**kwargs))
        response_kwargs = {}
        response_kwargs['content_type'] = 'application/json'

        return HttpResponse(json.dumps(data), content_type="application/json")
        # return redirect(self.get_object())

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        context['user_worksheet'] = QuestionSet.objects.user_worksheet(
            id=worksheet.id, user=self.request.user.id)
        return context


class QuestionSetResultsView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet_results.html'

    def get_context_data(self, **kwargs):
        context = super(
            QuestionSetResultsView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        context['user_worksheet'] = QuestionSet.objects.user_worksheet(
            id=worksheet.id, user=self.request.user.id)
        return context


class WorksheetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'formtest.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        worksheet = self.get_object()
        questions = QuestionSet.objects.questions(id=worksheet.id)
        WorksheetForm = formset_factory(
            form=QuestionForm, formset=QuestionSetForm)
        f = WorksheetForm(questions)
        return self.render_to_response(self.get_context_data(form=f))

    def post(self, request, *args, **kwargs):
        self.object = None
        worksheet = self.get_object()
        questions = QuestionSet.objects.questions(id=worksheet.id)
        WorksheetForm = formset_factory(
            form=QuestionForm, formset=QuestionSetForm)
        f = WorksheetForm(questions, request.POST)

        if f.is_valid():
            return render(request, self.template_name, {'feedback': 'thanks'})

        return render(request, self.template_name, self.get_context_data(form=f))
