# views.py
from collections import OrderedDict

from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from lessons.models import Lesson
from questions.models import QuestionSet

from .models import PretestUser, PretestQuestionResponse
from .forms import LoginTokenForm, PretestQuestionResponseForm, PretestQuestionResponseForm
from .mixins import TokenAccessRequiredMixin

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


class PretestMenuView(TokenAccessRequiredMixin, TemplateView):
    template_name = 'pretest_menu.html'

    """TODO: check for language setting to show form or not."""

    def get_context_data(self, **kwargs):
        context = super(PretestMenuView, self).get_context_data(**kwargs)
        context['lessons'] = [Lesson.objects.get(pk=18), Lesson.objects.get(pk=17)]
        return context


class PretestEndView(TokenAccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'pretest_end.html'
    
    def get(self, request, *args, **kwargs):
        # TODO: Before proceeding, check whether user should be seeing this question and adjust accordingly

        return super(PretestEndView, self).get(request, *args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super(PretestEndView, self).get_context_data(**kwargs)
        puser = get_object_or_404(PretestUser, pk=self.kwargs['user'])
        context['puser'] = puser
        context['responses'] = self.get_object().get_pretest_user_response_objects(puser)

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


class PretestQuestionResponseView(TokenAccessRequiredMixin, UpdateView):
    model = PretestQuestionResponse
    template_name = 'pretest_beta_question.html'
    form_class = PretestQuestionResponseForm
    pretestuser = None  # this is assigned in TokenAccessRequiredMixin or fail.
    worksheet = None
    question = None

    def dispatch(self, *args, **kwargs):
        self.worksheet = get_object_or_404(QuestionSet, pk=self.kwargs['p'])
        self.question = self.worksheet.get_question_at_index(int(self.kwargs['q']) - 1)

        return super(PretestQuestionResponseView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.question:
            return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)
        # TODO: Before proceeding, check whether user should be seeing this question and adjust accordingly
        
        return super(PretestQuestionResponseView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        question_type = self.question['question'].get_django_content_type()
        object_id = self.question['question'].id
        queryset = queryset.filter(pretestuser=self.pretestuser, content_type=question_type, object_id=object_id)
        
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return None
        return obj

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
        return reverse('pretests:pretest_take', args=[self.question['question'].question_set.id, next_item])

    def get_context_data(self, **kwargs):
        context = super(PretestQuestionResponseView, self).get_context_data(**kwargs)
        return context 
