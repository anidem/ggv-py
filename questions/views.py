# questions/views.py
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory
from django import forms
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin
from .models import QuestionSet, MultipleChoiceQuestion, ShortAnswerQuestion, QuestionResponse
from .forms import QuestionPostForm, MultipleChoiceQuestionForm, ShortAnswerQuestionForm


class QuestionSetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'questions_response_form.html'

    def post(self, request, *args, **kwargs):

        worksheet = self.get_object()
        worksheet_data = QuestionSet.objects.user_worksheet(
            id=worksheet.id, user=self.request.user.id)
        worksheet_formset = formset_factory(QuestionPostForm)
        formset = worksheet_formset(request.POST, initial=worksheet_data)

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

            print 'POST VALID--> ', kwargs
            return HttpResponseRedirect(reverse('worksheet_results', args=kwargs['pk']))

        print 'POST NOT VALID'
        return render(request, self.template_name, {'formset': formset, })

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        worksheet_data = QuestionSet.objects.user_worksheet(
            id=worksheet.id, user=self.request.user.id)

        worksheet_formset = formset_factory(QuestionPostForm, extra=0)
        formset = worksheet_formset(initial=worksheet_data)
        context['formset'] = formset
        # worksheet_formset = formset_factory(QuestionPostForm, extra=0)
        # context['formset'] = worksheet_formset(initial=self.initial)
        # print 'GET -- context -->', context

        return context



class QuestionSetResultsView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'questions_worksheet_results.html'

    def get_context_data(self, **kwargs):
        context = super(
            QuestionSetResultsView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        context['user_worksheet'] = QuestionSet.objects.user_worksheet(
            id=worksheet.id, user=self.request.user.id)
        return context


class QuestionSetScreenView(DetailView):
    pass


class CreateResponse(CreateView):
    model = QuestionResponse
    template_name = 'question.html'
    form_class = MultipleChoiceQuestionForm

    def get_initial(self):
        question_list = QuestionSet.objects.questions(id=self.kwargs['pk'])
        curr_question = question_list[int(self.kwargs['q'])]
        inits = {
            'question_type': curr_question.get_question_content_type(),
            'question_id': curr_question.id,
            'label' : curr_question,
            'choices': curr_question.get_options_map(),
            'user': self.request.user
        }
        return inits     

# ***
class QuestionResponseCreate(DetailView):
    model = QuestionSet
    template_name = 'question.html'

    def post(self, request, *args, **kwargs):
        QuestionForm = modelform_factory(QuestionResponse, form=MultipleChoiceQuestionForm)
        form = QuestionForm(request.POST)
        if form.is_valid():            
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
                
            print 'POST VALID--> ', kwargs
            return HttpResponseRedirect(reverse('worksheet_results', args=kwargs['pk']))

        print 'POST NOT VALID'
        return render(request, self.template_name, {'formset': formset, })

    def get_context_data(self, **kwargs):
        context = super(
            QuestionResponseCreate, self).get_context_data(**kwargs)

        question_list = QuestionSet.objects.questions(id=self.get_object().id)
        curr_question = question_list[int(self.kwargs['q'])]

        print curr_question.get_question_content_type()

        inits = {
            'question_type': curr_question.get_question_content_type(),
            'question_id': curr_question.id,
            'label' : curr_question,
            'choices': curr_question.get_options_map(),
            'user': self.request.user
        }

        QuestionForm = modelform_factory(QuestionResponse,
            form=MultipleChoiceQuestionForm,
            widgets={
                'response': forms.RadioSelect(choices=curr_question.get_options_map())
            },
            labels={'response': curr_question}
        )
        form = QuestionForm(initial=inits)
        context['form'] = form
        context['question'] = curr_question
        return context
