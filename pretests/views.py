# views.py
from collections import OrderedDict

from django.forms import ValidationError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from lessons.models import Lesson
from questions.models import QuestionSet

from .models import PretestUser, PretestQuestionResponse
from .forms import LoginTokenForm, LanguageChoiceForm, PretestQuestionResponseForm
from .mixins import TokenAccessRequiredMixin, PretestQuestionMixin

class PretestHomeView(FormView):
    template_name = 'pretest_home.html'
    form_class = LoginTokenForm

    def get(self, request, *args, **kwargs):
        try:
            token = self.request.session['pretester_token']
            pretester = PretestUser.objects.get(access_token=token)         
            return redirect('pretests:pretest_menu')
        except:
            pass
        
        return super(PretestHomeView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        # set up a session variable for the user. will need more sophistication here.
        # add token, add timestamp, add email???
        self.request.session['pretester_token'] = form.cleaned_data['token']

        return super(PretestHomeView, self).form_valid(form)

    def get_success_url(self):
        success_url = reverse('pretests:pretest_menu', current_app=self.request.resolver_match.namespace)
        return success_url

    def get_context_data(self, **kwargs):
        context = super(PretestHomeView, self).get_context_data(**kwargs)
        return context


class PretestLanguageChoiceUpdateView(TokenAccessRequiredMixin, UpdateView):
    model = PretestUser
    template_name = 'pretest_language_choice.html'
    form_class = LanguageChoiceForm
    
    def get(self, request, *args, **kwargs):
        if self.pretestuser.id != int(self.kwargs['pk']):
                return redirect('pretests:pretest_home')       
                
        return super(PretestLanguageChoiceUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self): 
        return reverse('pretests:pretest_menu', current_app=self.request.resolver_match.namespace)


class PretestMenuView(TokenAccessRequiredMixin, TemplateView):
    template_name = 'pretest_menu.html'

    """TODO: check for language setting to show form or not."""
    def get(self, request, *args, **kwargs):
        try:
            if not self.pretestuser.language_pref:
                return redirect('pretests:pretest_language_choice', pk=self.pretestuser.id)          
        except:
            return redirect('pretests:pretest_home')
        
        return super(PretestMenuView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PretestMenuView, self).get_context_data(**kwargs)
        if self.pretestuser.language_pref == 'spanish':
            context['lesson'] = Lesson.objects.get(pk=18)
        else:
            context['lesson'] = Lesson.objects.get(pk=17)
        
        return context


class PretestEndView(TokenAccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'pretest_end.html'
    
    def get(self, request, *args, **kwargs):
        return super(PretestEndView, self).get(request, *args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super(PretestEndView, self).get_context_data(**kwargs)
        context['pretestuser'] = get_object_or_404(PretestUser, pk=self.kwargs['user'])
        context['responses'] = self.get_object().get_pretest_user_response_objects(context['pretestuser'])
        return context


class PretestLogoutView(TemplateView):
    template_name = 'pretest_logout.html'

    def get(self, request, *args, **kwargs):
        try:
            del request.session['pretester_token']
        except KeyError:
            pass
        return super(PretestLogoutView, self).get(request, *args, **kwargs)


class PretestWorksheetLaunchView(TokenAccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'pretest_start.html'

    def get(self, request, *args, **kwargs):     
        return super(PretestWorksheetLaunchView, self).get(request, *args, **kwargs)


class PretestQuestionResponseView(TokenAccessRequiredMixin, PretestQuestionMixin, UpdateView):
    model = PretestQuestionResponse
    template_name = 'pretest_question.html'
    form_class = PretestQuestionResponseForm
    
    def get(self, request, *args, **kwargs):

        if self.request.user.is_staff:
            if not self.question:
                return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)
            return super(PretestQuestionResponseView, self).get(request, *args, **kwargs)            

        if self.stack['count'] >= len(self.stack['responses']):  # user has answered all questions so show results page.
            return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)
        
        elif not self.question: # request for invalid question so take user to next available question not answered.
            return redirect('pretests:pretest_take', p=self.worksheet.id, q=self.stack['count']+1)

        return super(PretestQuestionResponseView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.stack['responses'][self.req_question]

    def get_initial(self):
        initial = super(PretestQuestionResponseView, self).get_initial()
        initial['pretestuser'] = self.pretestuser
        initial['content_type'] = self.question['question'].get_django_content_type()
        initial['object_id'] = self.question['question'].id
        initial['question'] = self.question['question']

        return initial

    def form_valid(self, form):
        try:
            # strip whitespace from text question responses.
            if len(form.cleaned_data['response']) > 20:
                form.response = form.response.strip()
        except:
            pass
        
        self.object = form.save()
        return super(PretestQuestionResponseView, self).form_valid(form)

    def get_success_url(self):
        next_item = int(self.kwargs['q']) + 1
        return reverse('pretests:pretest_take', args=[self.worksheet.id, next_item], current_app=self.request.resolver_match.namespace)

    def get_context_data(self, **kwargs):
        context = super(PretestQuestionResponseView, self).get_context_data(**kwargs)
        context['question'] = self.question['question']
        context['question_position'] = self.req_question+1
        context['question_previous'] = self.req_question
        context['question_next'] = self.req_question+2
        context['question_count'] = len(self.stack['responses'])
        context['response_count'] = self.stack['count']

        return context 
