
from collections import OrderedDict
from datetime import datetime, date

from django.forms import ValidationError
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.text import slugify
from django.conf import settings

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin, JSONResponseMixin, AjaxResponseMixin
from openpyxl import Workbook

from lessons.models import Lesson
from questions.models import QuestionSet

from .models import PretestAccount, PretestUser, PretestQuestionResponse, PretestUserCompletion, PretestUserAssignment, ENG_PRETESTS_LESSON_ID, SPN_PRETESTS_LESSON_ID
from .forms import LoginTokenForm, LanguageChoiceForm, PretestQuestionResponseForm, PretestSelectionForm, PretestUserUpdateForm, PretestUserCreateForm, PretestCompleteConfirmForm, PretestResponseGradeForm
from .mixins import TokenAccessRequiredMixin, PretestQuestionMixin, PretestAccountRequiredMixin
from .utils import AccessErrorView
from .emails import send_request_to_grade, send_score_notification, send_completion_notification


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
        # set up a session variable for flagged questions.
        self.request.session['flags'] = {}

        return super(PretestHomeView, self).form_valid(form)

    def get_initial(self):
        initial = super(PretestHomeView, self).get_initial()
        try:
            token = self.kwargs['token']
            initial['email'] = PretestUser.objects.get(access_token=token).email
            initial['token'] = token            
        except:
            pass
        return initial

    def get_success_url(self):
        success_url = reverse('pretests:pretest_menu', current_app=self.request.resolver_match.namespace)
        return success_url

    def get_context_data(self, **kwargs):
        context = super(PretestHomeView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['pretest_accounts'] = PretestAccount.objects.all()
        elif self.request.user.is_authenticated:
            context['pretest_accounts'] = self.request.user.pretest_user_account.all()

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

    def get(self, request, *args, **kwargs):
        # reroute to language choice form if language preference is not set
        try:
            if not self.pretestuser.language_pref:
                return redirect('pretests:pretest_language_choice', pk=self.pretestuser.id)          
        except:
            return redirect('pretests:pretest_home')
        
        return super(PretestMenuView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PretestMenuView, self).get_context_data(**kwargs)
        assigned = self.pretestuser.pretest_assignments.all()
        if assigned:
            test_bundle = [i.pretest for i in assigned]
        
        # User was created prior to pretest update on aug 15
        # Retrieve tests based on spanish or english language preference
        elif self.pretestuser.created.date() < date(2017, 8, 15):
            if self.pretestuser.language_pref == 'spanish':
                test_bundle = Lesson.objects.get(pk=SPN_PRETESTS_LESSON_ID).activities()

            else:
                test_bundle = Lesson.objects.get(pk=ENG_PRETESTS_LESSON_ID).activities()

            # user created before modification unit update == > pretestuserassignment objects:
            for i in test_bundle:
                try:
                    p = PretestUserAssignment(pretestuser=self.pretestuser, pretest=i)
                    p.save()
                except IntegrityError as e:
                    # assignment map already exists
                    pass
        else:  # pretestuser account was created after update but does not have tests assigned.
            test_bundle = []

        completion_map = {i: (-2, -2) for i in test_bundle}

        for i in self.pretestuser.pretest_user_completions.all():
            if i.is_expired() or i.confirm_completed:
                completion_map[i.completed_pretest] = i.get_score()
            else:
                completion_map[i.completed_pretest] = (-1, -1) # indicates user has started an exam

        context['completions'] = completion_map
        return context


class PretestEndConfirmView(TokenAccessRequiredMixin, UpdateView):
    model = PretestUserCompletion
    template_name = 'pretest_confirm_complete.html'
    form_class = PretestCompleteConfirmForm
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(PretestEndConfirmView, self).get(request, *args, **kwargs)
        elif self.pretestuser.id != self.get_object().pretestuser.id:
            return redirect('pretests:pretest_home')
        else:               
            return super(PretestEndConfirmView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(PretestEndConfirmView, self).get_initial()
        initial['confirm_completed'] = True
        return initial

    def get_success_url(self): 
        return reverse('pretests:pretest_done', args=[self.get_object().completed_pretest.id, self.pretestuser.id], current_app=self.request.resolver_match.namespace)

    def get_context_data(self, **kwargs):
        context = super(PretestEndConfirmView, self).get_context_data(**kwargs)
        context['questions'] = self.get_object().completed_pretest.get_ordered_question_list()
        context['flags'] = [int(i) for i in self.request.session['flags'].keys()]
        return context


class PretestEndView(TokenAccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'pretest_end.html'
    
    def get(self, request, *args, **kwargs):
        return super(PretestEndView, self).get(request, *args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super(PretestEndView, self).get_context_data(**kwargs)
        context['pretestuser'] = get_object_or_404(PretestUser, pk=self.kwargs['user'])
        # context['responses'] = self.get_object().get_pretest_user_response_objects(context['pretestuser'])
        completion_obj = context['pretestuser'].pretest_user_completions.get(completed_pretest=self.get_object())
        
        if completion_obj:
            if not completion_obj.confirm_completed:
                completion_obj.confirm_completed = True
                completion_obj.save()

            responses = completion_obj.completed_pretest.get_pretest_user_response_objects(context['pretestuser'])
            context['completion'] = (completion_obj, responses['num_correct'] * 8, responses['responses'])
            
            graded = True
            for i in responses['responses']:
                if i and i.score == -1:  # indicates a response (essay question) needs to graded.
                    graded = False
                    send_request_to_grade(self.request, pretest_response_obj=i)

            if graded:
                send_completion_notification(self.request, pretest_completion_obj=completion_obj)
        
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
        
        # user has already confirmed completed pretest.
        if self.status_obj.confirm_completed:
            return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)

        # user has answered all questions (they are requesting a null question). show confirm page.
        elif self.req_question+1 > self.worksheet.get_num_questions():
            return redirect('pretests:pretest_confirm_done', pk=self.status_obj.id)
        
        # request for invalid question so take user to next available question not answered.
        elif not self.question:
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
            if form.instance.content_object.get_question_type() == 'text':
                form.instance.score = -1  # indicates response needs to be graded (assigned a score)
                form.instance.iscorrect = False
        except Exception as e:
            pass  
        
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
        
        if self.stack['count'] >= len(self.stack['responses']):
            context['status'] = self.status_obj

        if self.worksheet.id == 150 and context['question_position'] > 7:   # English pretest math.
            context['calculator'] = settings.MEDIA_URL + 'pdf/0-calculator-eng.pdf'
            context['formula'] = settings.MEDIA_URL + 'pdf/0_A-GGV_Formula_Sheet_Eng.pdf'
        elif self.worksheet.id == 154 and context['question_position'] > 7:  # Spanish pretest math.
            context['calculator'] = settings.MEDIA_URL + 'pdf/0-calculator-spn.pdf'
            context['formula'] = settings.MEDIA_URL + 'pdf/0_A-GGV_Formula_Sheet_Spn.pdf'

        try:
            flags = self.request.session['flags']
            context['flag'] = flags[str(self.question['question'].id)]  
        except:
            pass
      
        # datetime.strftime(time_started, '%Y-%m-%d %H:%M:%S') maybe useful later.

        return context


class PretestToggleFlagView(TokenAccessRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        data = {}
        try:
            question = request.POST.get('flagged')
            del self.request.session['flags'][question]
            self.request.session.save()

        except Exception as e:
            question = request.POST.get('flagged')
            self.request.session['flags'][question] = True
            self.request.session.save()            

        return self.render_json_response(data)


###############################################################################
###############################################################################
######################### Account Manager Views ###############################
###############################################################################
###############################################################################


class PretestUserDetailView(LoginRequiredMixin, PretestAccountRequiredMixin, DetailView):
    model = PretestUser
    template_name = 'pretest_user_detail.html'
    pretest_accounts = None
    access_model = PretestUser

    def get_context_data(self, **kwargs):
        context = super(PretestUserDetailView, self).get_context_data(**kwargs)        
        context['pretest_accounts'] = self.pretest_accounts
        context['bundle'] = self.get_object().pretest_bundle()
        completions = []
        for i in self.get_object().completion_status():
            responses = i.completed_pretest.get_pretest_user_response_objects(i.pretestuser)
            completions.append((i, responses['num_correct'] * 8, responses['responses']))
        context['completions'] = completions
        return context


class PretestUserCreateView(LoginRequiredMixin, CreateView):
    model = PretestUser
    template_name = 'pretest_user_create.html'
    form_class = PretestUserCreateForm

    def get(self, request, *args, **kwargs):
        self.account = PretestAccount.objects.get(pk=kwargs.get('account'))
        if request.user.pk == self.account.manager.pk or request.user.is_staff:
            return super(PretestUserCreateView, self).get(request, *args, **kwargs)
        return redirect('pretests:pretest_access_error')

    def post(self, request, *args, **kwargs):
        self.account = PretestAccount.objects.get(pk=kwargs.get('account'))
        if request.user.pk == self.account.manager.pk or request.user.is_staff:
            return super(PretestUserCreateView, self).post(request, *args, **kwargs)
        return redirect('pretests:pretest_access_error')

    def get_initial(self):
        initial = super(PretestUserCreateView, self).get_initial()
        try:
            self.user_list = self.account.get_org_users()
            initial['users'] = self.user_list
        except:
            initial['users'] = []

        initial['account'] = self.account
        
        return initial

    def form_valid(self, form):
        # Gather selected pretests to map to pretestuser object. 
        selector_form = PretestSelectionForm(self.request.POST)
        if selector_form.is_valid():
            try:
                selected_pretests = []
                selected_pretests.extend(selector_form.cleaned_data['eng_pretests'])
                selected_pretests.extend(selector_form.cleaned_data['spn_pretests'])       

                max_tests = self.account.tests_purchased           
                pretests_in_use = self.account.get_pretest_assignments().count()
                pretests_in_use = pretests_in_use + len(selected_pretests)

                # Verify that requests for pretests is within quota.
                if pretests_in_use > max_tests:
                    messages.error(self.request, 'Pretest user token not added. The number of selected pretests exceeds purchased pretests.')
                    return super(PretestUserCreateView, self).form_invalid(form) 
                
                # Verify that at least one pretest is selected.
                if len(selected_pretests) == 0:
                    messages.error(self.request, 'Please select one or more pretest exams for this user.')
                    return super(PretestUserCreateView, self).form_invalid(form)

                # Save the pretestuser object.
                self.object = form.save()                
                
                # Assign pretests to new pretester 
                for i in selected_pretests:
                    try:                
                        pretest_obj = QuestionSet.objects.get(pk=i)
                        p = PretestUserAssignment(pretestuser=self.object, pretest=pretest_obj)
                        p.save()
                    except IntegrityError as duplicate:
                        pass
            
            except Exception as e:
                return super(PretestUserCreateView, self).form_invalid(form)

            messages.success(self.request, 'Pretest user token successfully added.')
            return super(PretestUserCreateView, self).form_valid(form)
        else:
            # selector_form not valid.
            return super(PretestUserCreateView, self).form_invalid(form)

    def get_success_url(self): 
        return reverse('pretests:pretest_user_list', args=[self.object.account.id], current_app=self.request.resolver_match.namespace)

    def get_context_data(self, **kwargs):
        context = super(PretestUserCreateView, self).get_context_data(**kwargs)
        try:
            context['user_list'] = self.user_list
            context['google_db'] = self.account.ggv_org.google_db.all()[0]            
        except:
            pass
        context['account'] = self.account
        assigned = self.account.get_pretest_assignments().count()
        context['pretest_stat'] = {
            'purchased': self.account.tests_purchased, 
            'used': assigned,
            'available': self.account.tests_purchased - assigned
        }
        context['pretest_selector'] = PretestSelectionForm()
        return context


class PretestUserUpdateView(LoginRequiredMixin, PretestAccountRequiredMixin, UpdateView):
    model = PretestUser
    template_name = 'pretest_user_edit.html'
    form_class = PretestUserCreateForm
    pretest_accounts = None
    access_model = PretestUser

    def get(self, request, *args, **kwargs):
        self.account =  self.get_object().account

        # load completed (or started) pretests for the user
        self.completed = [str(i.completed_pretest.pk) for i in self.get_object().pretest_user_completions.all()]
        return super(PretestUserUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.account =  self.get_object().account
        
        # load completed (or started) pretests for the user
        self.completed = [str(i.completed_pretest.pk) for i in self.get_object().pretest_user_completions.all()]
        return super(PretestUserUpdateView, self).post(request, *args, **kwargs)

    def get_initial(self):
        initial = super(PretestUserUpdateView, self).get_initial()
        try:
            self.user_list = self.get_object().account.get_org_users()
            initial['users'] = self.user_list
        except:
            initial['users'] = []
        return initial

    def form_valid(self, form):
        # Gather user's previously assigned pretests.
        prev_pretest_data = self.get_object().pretest_assignments.all()
        data = {}
        data['eng_pretests'] = [i.pretest.pk for i in prev_pretest_data.filter(pretest__lesson__pk=ENG_PRETESTS_LESSON_ID)]
        data['spn_pretests'] = [i.pretest.pk for i in prev_pretest_data.filter(pretest__lesson__pk=SPN_PRETESTS_LESSON_ID)]
        
        selector_form = PretestSelectionForm(self.request.POST, initial=data)

        if selector_form.has_changed():
            if selector_form.is_valid():
                # Gather selected pretests to map to pretestuser object. 
                updated_pretests = selector_form.cleaned_data['eng_pretests']
                updated_pretests.extend(selector_form.cleaned_data['spn_pretests'])
                updated_pretests.extend(self.completed)
                
                max_tests = self.account.tests_purchased
                diff = len(updated_pretests) - prev_pretest_data.count()                
                pretests_in_use = self.account.get_pretest_assignments().count()                
                pretests_in_use = pretests_in_use + diff
                                
                if pretests_in_use <= max_tests:
                    self.get_object().pretest_assignments.all().delete()
                    # Assign pretests to pretester 
                    for i in updated_pretests:
                        try:                
                            pretest_obj = QuestionSet.objects.get(pk=i)
                            p = PretestUserAssignment(pretestuser=self.get_object(), pretest=pretest_obj)
                            p.save()
                        except IntegrityError as duplicate:
                            pass
                else:
                    messages.error(self.request, 'Pretest user token not updated. The number of selected pretests exceeds purchased pretests.')
                    return super(PretestUserUpdateView, self).form_invalid(form)                  

        messages.success(self.request, 'User successfully updated.')
        return super(PretestUserUpdateView, self).form_valid(form)

    def get_success_url(self): 
        return reverse('pretests:pretest_user_list', args=[self.get_object().account.id], current_app=self.request.resolver_match.namespace)

    def get_context_data(self, **kwargs):
        context = super(PretestUserUpdateView, self).get_context_data(**kwargs)
        try:
            context['user_list'] = self.user_list
            context['google_db'] = self.account.ggv_org.google_db.all()[0]
        except:
            pass
        
        
        # load previously selected pretest assignments
        pretests = self.get_object().pretest_assignments.all()
        data = {}
        data['eng_pretests'] = [i.pretest.pk for i in pretests.filter(pretest__lesson__pk=ENG_PRETESTS_LESSON_ID)]
        data['spn_pretests'] = [i.pretest.pk for i in pretests.filter(pretest__lesson__pk=SPN_PRETESTS_LESSON_ID)]
        selector_form = PretestSelectionForm(initial=data)

        assigned = self.get_object().account.get_pretest_assignments().count()
        context['pretest_stat'] = {
            'purchased': self.get_object().account.tests_purchased, 
            'used': assigned,
            'available': self.get_object().account.tests_purchased - assigned
        }

        context['assigned'] = [str(i.pretest.pk) for i in pretests]
        context['completed'] = self.completed
        context['pretest_selector'] = selector_form
        return context


class PretestUserCreateFromGoogleView(PretestUserCreateView):
    template_name = 'pretest_user_create_from_google.html'

    def get_initial(self):
        initial = super(PretestUserCreateFromGoogleView, self).get_initial()
        initial['users'] = []  # Clear user list b/c list will load from google spreadsheet
        return initial

    def get_context_data(self, **kwargs):
        context = super(PretestUserCreateFromGoogleView, self).get_context_data(**kwargs)
        try:
            context['google_db'] = self.account.ggv_org.google_db.all()[0]
        except:
            pass

        return context


class PretestUserUpdateFromGoogleView(PretestUserUpdateView):
    template_name = 'pretest_user_edit_from_google.html'

    def get_initial(self):
        initial = super(PretestUserUpdateFromGoogleView, self).get_initial()
        initial['users'] = []  # Clear user list b/c list will load from google spreadsheet
        return initial

    def get_context_data(self, **kwargs):
        context = super(PretestUserUpdateFromGoogleView, self).get_context_data(**kwargs)
        try:
            context['google_db'] = self.account.ggv_org.google_db.all()[0]
        except:
            pass

        return context

# class PretestUserAssignmentUpdate(LoginRequiredMixin, PretestAccountRequiredMixin, UpdateView):


class PretestAccountListView(LoginRequiredMixin, PretestAccountRequiredMixin, TemplateView):
    template_name = "pretest_account_list.html"
    pretest_accounts = None
    access_model = User

    def get_context_data(self, **kwargs):
        context = super(PretestAccountListView, self).get_context_data(**kwargs)
        context['pretest_accounts'] = self.pretest_accounts
        return context


class PretestUserListView(LoginRequiredMixin, PretestAccountRequiredMixin, DetailView):
    model = PretestAccount
    template_name = "pretest_user_list.html"
    pretest_accounts = None
    access_model = PretestAccount

    def get(self, request, *args, **kwargs):           
        return super(PretestUserListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PretestUserListView, self).get_context_data(**kwargs)        
        context['account'] = self.get_object()
        context['pretest_users'] = context['account'].pretest_user_list()
        context['pretest_accounts'] = self.pretest_accounts

        assigned = self.get_object().get_pretest_assignments().count()
        context['pretest_stat'] = {
            'purchased': self.get_object().tests_purchased, 
            'used': assigned,
            'available': self.get_object().tests_purchased - assigned
        }
        return context


class PretestAccountReportView(DetailView):
    model = PretestAccount
    template_name = "pretest_user_score_list.html"
    
    def get(self, request, *args, **kwargs):                
        return super(PretestAccountReportView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PretestAccountReportView, self).get_context_data(**kwargs)
        account = self.get_object()
        scores = []
        for i in account.tokens.filter(email__isnull=False).order_by('email'):
            for j in i.pretest_user_completions.all():
                datarow = [i.program_id, j.completed_pretest.title, j.get_score()[0], datetime.strftime(j.created, '%m/%d/%Y')]
                scores.append(datarow)
        context['scores'] = scores
        return context


class PretestAccountReportProtectedView(LoginRequiredMixin, DetailView):
    model = PretestAccount
    template_name = "pretest_user_score_list_protected.html"
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super(PretestAccountReportProtectedView, self).get(request, *args, **kwargs)
        elif not self.get_object().ggv_org:
            return redirect('pretests:pretest_access_error')
        
        org_staff = self.get_object().ggv_org.instructor_list() + self.get_object().ggv_org.manager_list() + [self.get_object().manager]
        if self.request.user not in org_staff:
            return redirect('pretests:pretest_access_error')

        return super(PretestAccountReportProtectedView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PretestAccountReportProtectedView, self).get_context_data(**kwargs)
        account = self.get_object()
        scores = []
        for i in account.tokens.filter(email__isnull=False).order_by('email'):
            for j in i.pretest_user_completions.all():
                datarow = [i.program_id, i.first_name, i.last_name, j.completed_pretest.title, j.get_score()[0], datetime.strftime(j.created, '%m/%d/%Y')]
                scores.append(datarow)
        context['scores'] = scores
        return context


class PretestResponseGradeView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    model = PretestQuestionResponse
    template_name = 'pretest_grade_response.html'
    form_class = PretestResponseGradeForm

    def get_success_url(self):
        messages.info(self.request, 'Your assessment has been saved.')
        send_score_notification(self.request, self.get_object())
        return reverse('pretests:pretest_response_grade', args=[self.get_object().id], current_app=self.request.resolver_match.namespace)

    def get_context_data(self, **kwargs):
        context = super(PretestResponseGradeView, self).get_context_data(**kwargs)
        context['question'] =  self.get_object().content_object
        return context 





