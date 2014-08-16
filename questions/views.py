# questions/views.py
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory
from django import forms
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin
from .models import QuestionSet, MultipleChoiceQuestion, ShortAnswerQuestion, QuestionResponse
from .forms import QuestionPostForm, MultipleChoiceQuestionForm, ShortAnswerQuestionForm

# process json question data imports
import json

class ImportQuestionDataView(DetailView):
    model = QuestionSet
    
    def get_context_data(self, **kwargs):
        context = super(ImportQuestionDataView, self).get_context_data(**kwargs)
        #This should load a preprocessed json file and write to the db with json values.
        # SEE: question_builder.py
        # json_file = open('static/question1.json')
        # json_data = json_file.read()
        # data1 = json.loads(json_data) 
              
        # for i in data1:
        #     for key, value in i.iteritems():
        #         print '%s ==> %s' % (key, value)


        # json_file.close()
        # print data1
           

class WorksheetHomeView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'worksheet.html'

class QuestionSetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'questions_full_form.html'

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
        print worksheet_data
        worksheet_formset = formset_factory(QuestionPostForm, extra=0)
        formset = worksheet_formset(initial=worksheet_data)
        context['formset'] = formset
        # worksheet_formset = formset_factory(QuestionPostForm, extra=0)
        # context['formset'] = worksheet_formset(initial=self.initial)
        # print 'GET -- context -->', context

        return context

class QuestionResponseView(DetailView):
    model = QuestionSet
    template_name = 'question.html'

    def post(self, request, *args, **kwargs):
        question_type = ContentType.objects.get(id=request.POST['question_type'])
        current_question = question_type.get_object_for_this_type(id=request.POST['question_id'])
        
        if current_question.get_question_type() == 'multiplechoicequestion':
            form = MultipleChoiceQuestionForm(request.POST)
            form.fields['response'].widget = forms.RadioSelect(choices=current_question.get_options_as_list()) 
        else:
            form = ShortAnswerQuestionForm(request.POST)
        
        form.fields['response'].label = current_question
        
        resp = None

        if form.is_valid():
            try:
                # check for previous response
                resp = current_question.responses.get(user=request.user)
                if resp.response != form.cleaned_data['response']:
                    resp.response = form.cleaned_data['response']
                    resp.save()
            except:
                resp = QuestionResponse()
                resp.user = request.user
                resp.response = form.cleaned_data['response']
                resp.question_type = form.cleaned_data['question_type']
                resp.question_id = current_question.id
                resp.content_object = current_question
                resp.save()

                
        qindex = int(self.kwargs['q'])
        redisplay = {}
        redisplay['form'] = form
        redisplay['object'] = self.get_object()
        redisplay['questions'] = QuestionSet.objects.worksheet_report(worksheet=self.get_object(), user=self.request.user)
        redisplay['active'] = qindex
        redisplay['prev'] = qindex - 1
        redisplay['next'] = qindex + 1

        if resp:
            redisplay['response'] = resp
            redisplay['correct'] = resp.response in current_question.get_correct_answer()

        return render(self.request, self.template_name, redisplay)

    def get_context_data(self, **kwargs):
        context = super(
            QuestionResponseView, self).get_context_data(**kwargs)

        qindex = int(self.kwargs['q'])
        questions = QuestionSet.objects.worksheet_report(worksheet=self.get_object(), user=self.request.user)

        try:
            if qindex == 0:
                raise NameError('bad index')
            current = questions[qindex-1]
            current_question = current['question']
            current_question_type_name = current_question.get_question_content_type().model
        except:
            context['questions'] = questions
            context['active'] = qindex
            return context
        
        form_inits = {
            'question_type': current_question.get_question_content_type(),
            'question_id': current_question.id,
        }

        if current_question_type_name == 'multiplechoicequestion':
            form = MultipleChoiceQuestionForm(initial=form_inits)
            form.fields['response'].widget = forms.RadioSelect(choices=current_question.get_options_as_list())       
        else:
            form = ShortAnswerQuestionForm(initial=form_inits)     
        
        form.fields['response'].label = current_question
        form.fields['response'].initial =  current['response']

        try:
            context['correct'] = current['correct']
        except:
            pass

        context['form'] = form
        context['questions'] = questions        
        context['response'] = current['response']
        context['active'] = qindex
        context['prev'] = qindex - 1
        context['next'] = qindex + 1
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