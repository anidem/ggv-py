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
class QuestionResponseView(DetailView):
    model = QuestionSet
    template_name = 'question.html'

    def post(self, request, *args, **kwargs):
        question_type = ContentType.objects.get(id=request.POST['question_type'])
        current_question = question_type.get_object_for_this_type(id=request.POST['question_id'])
        form = MultipleChoiceQuestionForm(request.POST)
                 
        if form.is_valid():
            # question = form.cleaned_data['question_type'].get_object_for_this_type(
            #     pk=form.cleaned_data['question_id'])
            try:
                # check for previous response
                resp = current_question.responses.get(user=request.user)
                if resp.response != form.cleaned_data['response']:
                    resp.response = form.cleaned_data['response']
                    resp.save()
            except:
                resp = QuestionResponse()
                resp.user = request.user
                resp.response = form.cleaned_data['response'] or None
                resp.question_type = form.cleaned_data['question_type']
                resp.question_id = current_question.id
                resp.content_object = current_question
                resp.save()
                
            print 'POST VALID--> '
            self.kwargs['q'] = int(kwargs['q'])+1

            return HttpResponseRedirect(reverse('question', kwargs=self.kwargs))

        else:
            form.fields['response'].label = current_question
            form.fields['response'].widget.choices = current_question.get_options_as_list()
            print 'POST NOT VALID-> ',  form
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(
            QuestionResponseView, self).get_context_data(**kwargs)

        questions = QuestionSet.objects.questions(id=self.get_object().id)
        
        try:
            current_question = questions[int(self.kwargs['q'])]
        except:
            return HttpResponseRedirect(reverse('worksheet_results', args=kwargs['pk']))

        form_inits = {
            'question_type': current_question.get_question_content_type(),
            'question_id': current_question.id,
            # 'question_prompt': current_question,
            # 'user': self.request.user
        }

        current_question_type = current_question.get_question_content_type().model
        
        if current_question_type == 'multiplechoicequestion':
            # form_inits['choices'] = current_question.get_options_as_list()
            form = MultipleChoiceQuestionForm(initial=form_inits)
            form.fields['response'].widget.choices = current_question.get_options_as_list()
        else:
            form = ShortAnswerQuestionForm(initial=form_inits)
        
        form.user = self.request.user
        form.fields['response'].label = current_question
        
        context['form'] = form
        return context
