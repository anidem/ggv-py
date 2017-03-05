# views.py
from collections import OrderedDict
from datetime import datetime

from django.forms import ValidationError
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from lessons.models import Lesson
from questions.models import QuestionSet

from .models import PretestAccount, PretestUser, PretestQuestionResponse, PretestUserCompletion
from .forms import LoginTokenForm, LanguageChoiceForm, PretestQuestionResponseForm, PretestUserUpdateForm
from .mixins import TokenAccessRequiredMixin, PretestQuestionMixin
from .utils import AccessErrorView


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


class PretestUserUpdateView(UpdateView):
    model = PretestUser
    template_name = 'pretest_user_edit.html'
    form_class = PretestUserUpdateForm

    def get_success_url(self): 
        return reverse('pretests:pretest_user_list', current_app=self.request.resolver_match.namespace)


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


class PretestUserListView(TemplateView):
    template_name = "pretest_user_list.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user or not self.request.user.is_staff:
            return redirect('pretests:pretest_access_error')       
                
        return super(PretestUserListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PretestUserListView, self).get_context_data(**kwargs)
        try:
            account = PretestAccount.objects.get(manager=self.request.user)
        except:
            return redirect('pretests:pretest_access_error') 
            
        context['account'] = account
        context['pretest_users'] = account.pretest_user_list()
        return context


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
        
        completions = self.pretestuser.pretest_user_completions.all()

        context['completions'] = [i.completed_pretest.id for i in completions if i.is_expired()]
        context['incompletions'] = [i.completed_pretest.id for i in completions if not i.is_expired()]
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
        context['status_obj'] = context['pretestuser'].pretest_user_completions.filter(completed_pretest=self.get_object())
        context["score"] = [0, 0]
        for i in context['responses']['responses']:
            if i and i.iscorrect:
                context["score"][0] += 8
            context["score"][1] += 8
        
        return context


class PretestLogoutView(TemplateView):
    template_name = 'pretest_logout.html'

    def get(self, request, *args, **kwargs):
        for i in request.session.keys():
            try:
                del request.session[i]
            except KeyError:
                pass

        return super(PretestLogoutView, self).get(request, *args, **kwargs)


class PretestWorksheetLaunchView(TokenAccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'pretest_start.html'

    def get(self, request, *args, **kwargs):
        try:
            status_obj = self.pretestuser.pretest_user_completions.get(completed_pretest=self.get_object())
            if status_obj.is_expired(): 
                return redirect('pretests:pretest_done', pk=self.get_object().id, user=self.pretestuser.id)
            else:
                return redirect('pretests:pretest_take', p=self.get_object().id, q=1)

        except PretestUserCompletion.DoesNotExist:  # user will be starting the pretest for first time. show the launch page.
            pass

        return super(PretestWorksheetLaunchView, self).get(request, *args, **kwargs)


class PretestQuestionResponseView(TokenAccessRequiredMixin, PretestQuestionMixin, UpdateView):
    model = PretestQuestionResponse
    template_name = 'pretest_question.html'
    form_class = PretestQuestionResponseForm
    time_remaining = 0
    
    def get(self, request, *args, **kwargs):

        if self.request.user.is_staff:
            if not self.question:
                return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)
            return super(PretestQuestionResponseView, self).get(request, *args, **kwargs)            
        
        # try:
        #     status_obj = self.pretestuser.pretest_user_completions.get(completed_pretest=self.worksheet)          
        #     elapsed_time_secs = status_obj.seconds_since_created()
        
        # #  create a new completion record. user must be beginning the test
        # except PretestUserCompletion.DoesNotExist:  
        #     status_obj = PretestUserCompletion(pretestuser=self.pretestuser, completed_pretest=self.worksheet)
        #     status_obj.save()
        #     elapsed_time_secs = 0

        # #  completion record indicates that user has exceeded the time limit. show results page.
        # if elapsed_time_secs > self.worksheet.time_limit * 60: 
        #         return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)   
        
        # user has answered all questions. show results page.
        if self.stack['count'] >= len(self.stack['responses']):  
            return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)
       
        # request for invalid question so take user to next available question not answered.
        elif not self.question: 
            return redirect('pretests:pretest_take', p=self.worksheet.id, q=self.stack['count']+1)

        # self.time_remaining = self.worksheet.time_limit*60 - elapsed_time_secs   

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
        context['time_remaining'] = self.time_remaining
        context['pretestuser'] = self.pretestuser
        # datetime.strftime(time_started, '%Y-%m-%d %H:%M:%S') maybe useful later.

        return context 
