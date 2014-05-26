# questions/views.py
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView, FormView
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory, BaseModelFormSet
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
import json

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin
from .models import QuestionSet, MultipleChoiceQuestion, ShortAnswerQuestion, QuestionResponse
# from .forms import QuestionSetForm, QuestionForm

class QuestionSetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet.html'
    questions = []

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        # context['questions'] = QuestionSet.objects.questions(id=worksheet.id)
        context['user_worksheet'] = QuestionSet.objects.user_worksheet(id=worksheet.id, user=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        clean_request = request.POST.copy()
        clean_request.pop('csrfmiddlewaretoken')
        question_count = len(QuestionSet.objects.questions(id=self.get_object().id))
        messages = []
        errors = []
        data = dict()

        app = 'questions'
        # if len(clean_request) < question_count:

        #     errors.append('Please answer all questions. :)')
        #     data['errors'] = errors
        #     return HttpResponse(json.dumps(data), content_type="application/json")

        for i in clean_request:
            question_model = i[i.find('-') + 1:i.find('_')]
            question_id = i[i.find('_') + 1:]
            question_type = ContentType.objects.get(app_label=app, model=question_model)
                        
            question = question_type.get_object_for_this_type(pk=question_id)
            print question.id
            try:
                resp = QuestionResponse.objects.filter(
                    user=request.user).get(content_object=question)
                print resp
                if resp.response != request.POST[i]:
                    resp.response = request.POST[i]
                    resp.save()
                print 'response exists'
            except:

                resp = QuestionResponse()
                resp.user = request.user
                resp.response = request.POST[i]
                resp.content_type = question_type 
                resp.object_id = question.id
                resp.save()                
                resp.content_object = question
                
                resp.save()




    # user = models.ForeignKey(User)
    # response = models.TextField()
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # content_object = generic.GenericForeignKey('content_type', 'object_id')

        
        messages.append('Thanks!')
        data['messages'] = messages
        print 'THanks'
        return HttpResponse(json.dumps(data), content_type="application/json")
        # return HttpResponseRedirect(reverse('worksheet_results', args=(self.get_object().id,)))

class QuestionSetResultsView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet_results.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionSetResultsView, self).get_context_data(**kwargs)
        worksheet = self.get_object()
        context['user_worksheet'] = QuestionSet.objects.user_worksheet(id=worksheet.id, user=self.request.user.id)
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






