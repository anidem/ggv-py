from django.shortcuts import render
from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from .models import Survey, SurveyQuestionResponse
from .forms import SurveyQuestionResponseForm

class SurveyQuestionResponseView(UpdateView):
    model = SurveyQuestionResponse
    template_name = 'survey_question.html'
    form_class = SurveyQuestionResponseForm
    
    def get(self, request, *args, **kwargs):
        return super(SurveyQuestionResponseView, self).get(request, *args, **kwargs)

    # def get_initial(self):
    #     initial = super(SurveyQuestionResponseView, self).get_initial()
    #     initial['user'] = self.request.user
    #     initial['content_type'] = self.get_object().get_django_content_type()
    #     initial['object_id'] = self.get_object().id
    #     initial['question'] = self.get_object()
    #     return initial

    def get_object(self, queryset=None):
        return None

    def form_valid(self, form):       
        return super(SurveyQuestionResponseView, self).form_valid(form)

    def get_success_url(self):
    	pass
        # next_item = int(self.kwargs['q']) + 1
        # return reverse('pretests:pretest_take', args=[self.worksheet.id, next_item], current_app=self.request.resolver_match.namespace)

    def get_context_data(self, **kwargs):
        context = super(SurveyQuestionResponseView, self).get_context_data(**kwargs)
        context['question'] = self.get_object()
        # context['question'] = self.question['question']
        # context['question_position'] = self.req_question+1
        # context['question_previous'] = self.req_question
        # context['question_next'] = self.req_question+2
        # context['question_count'] = len(self.stack['responses'])
        # context['response_count'] = self.stack['count']
        # context['time_remaining'] = self.time_remaining
        # context['pretestuser'] = self.pretestuser
        return context
