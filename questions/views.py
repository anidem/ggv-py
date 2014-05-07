# questions/views.py
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory, BaseModelFormSet
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
import json

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin
from .models import QuestionSet, SimpleQuestion, QuestionResponse
from .forms import QuestionSetForm, QuestionForm


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


class QuestionSetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        context['questions'] = QuestionSet.objects.questions(
            id=self.get_object().id)
        return context

    def post(self, request, *args, **kwargs):
        clean_request = request.POST.copy()
        clean_request.pop('csrfmiddlewaretoken')
        worksheet = QuestionSet.objects.get(pk=self.get_object().id)
        return_data = dict()

        if len(clean_request) < QuestionSet.objects.questions(id=worksheet.id).count():
            return_data['error_msg'] = 'Please answer all questions. :)'
            return HttpResponse(json.dumps(return_data), content_type="application/json")

        for i in clean_request:
            question = SimpleQuestion.objects.get(pk=i[i.find('_') + 1:])
            try:
                resp = QuestionResponse.objects.filter(
                    user=request.user).get(question__id=question.id)
                if resp.response != request.POST[i]:
                    resp.response = request.POST[i]
                    resp.save()

            except QuestionResponse.DoesNotExist:
                resp = QuestionResponse()
                resp.user = request.user
                resp.worksheet = worksheet
                resp.question = question
                resp.response = request.POST[i]
                resp.save()
        
        return_data["success"] = 'Thanks!'
        return HttpResponse(json.dumps(return_data), content_type="application/json")

