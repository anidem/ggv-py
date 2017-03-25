# pretests/mixins.py

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from questions.models import QuestionSet
from .models import PretestUser, PretestUserCompletion, PretestAccount

class PretestAccountRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """Permission checks here rest on 
        a) braces.LoginRequiredMixin called prior to this mixin
        b) user object having an association with a pretest account object.

        Mixin primary function is to set class variable pretest_accounts (a listing of accounts. all for staff, filtered list for users)
        """
        access_model = self.access_model.__name__
        try:
            if self.request.user.is_staff:
                #  staff can access anything.
                self.pretest_accounts = PretestAccount.objects.all()
                return super(PretestAccountRequiredMixin, self).dispatch(*args, **kwargs)
           
            self.pretest_accounts = self.request.user.pretest_user_account.all()
            
            valid_account = None
            custom_message = 'any accounts.'
            if access_model == 'PretestAccount':
                #  user requesting access to an account information.
                #  user MUST have association with the account.
                valid_account = self.pretest_accounts.filter(pk=self.get_object().id)
                custom_message = str(self.get_object())
            
            elif access_model == 'PretestUser':
                #  user is requesting access to pretest user information (tokens and results).
                #  user must have association with the account associated with the pretest user account.
                valid_account = self.pretest_accounts.filter(pk=self.get_object().account.id)
                custom_message = 'token ' + str(self.get_object())

            elif access_model == 'QuestionSet':
                #  user is requesting to view detail results of pretest user score.
                userid=self.kwargs['user']
                pretestuser = PretestUser.objects.get(pk=userid)
                valid_account = self.pretest_accounts.filter(pk=pretestuser.account.id) 

            elif access_model == 'User':
                #  user is requesting a listing of their accounts.
                valid_account = self.pretest_accounts       

            if valid_account:
                return super(PretestAccountRequiredMixin, self).dispatch(*args, **kwargs)


            messages.error(self.request, 'You do not appear to have valid access to ' + custom_message, extra_tags='danger')
            return redirect('pretests:pretest_access_error')

        except Exception as e:
            print e, 'bad account'
            return redirect('pretests:pretest_access_error') 

class TokenAccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """Permission checks here rely on session variable pretester_token.

        This mixin effectively sets a pretestuser variable for the object.
        """
        try:
            token = self.request.session['pretester_token']
            self.pretestuser = PretestUser.objects.get(access_token=token)
            return super(TokenAccessRequiredMixin, self).dispatch(*args, **kwargs)
        
        except Exception as e:
            # print e
            if self.request.user.is_staff:
                return super(TokenAccessRequiredMixin, self).dispatch(*args, **kwargs)
            messages.error(self.request, 'You will need to provide your credentials to continue.', extra_tags='danger')
            return redirect('pretests:pretest_home')

class PretestQuestionMixin(object):

    def dispatch(self, *args, **kwargs):

        """Mixin to ensure that worksheet and question variables are initialized.
        This mixin should be used with views that require access to QuestionSet
        objects and Question objects.

        This mixin will set the following variables and must ensure that 
        TokenAccessRequiredMixin is executed first, setting the pretestuser object.

        worksheet - a QuestionSet object
        question - a question object as a child of worksheet.

        """
        try:
            if not self.pretestuser:
                token = self.request.session['pretester_token']
                self.pretestuser = PretestUser.objects.get(access_token=token)

            self.worksheet = get_object_or_404(QuestionSet, pk=kwargs['p'])
            self.stack = self.worksheet.get_pretest_user_response_objects(self.pretestuser)
            self.req_question = int(kwargs['q'])
            self.status_obj = None
            
            if self.req_question > 0: self.req_question -= 1
            else: self.req_question = 0

            # route staff differently because restriction on previously answered questions is lifted.
            if self.request.user.is_staff:
                if self.req_question < len(self.stack['responses']):
                    self.question = self.worksheet.get_question_at_index(self.req_question)
                else:
                    self.question = None

            # route to a previously answered question or send a null question object
            elif self.req_question <= self.stack['count']:
                self.question = self.worksheet.get_question_at_index(self.req_question)
            
            else:
                self.question = None

            try:
                self.status_obj = self.pretestuser.pretest_user_completions.get(completed_pretest=self.worksheet)          
                elapsed_time_secs = self.status_obj.seconds_since_created()
            
            #  create a new completion record. user must be beginning the test
            except PretestUserCompletion.DoesNotExist:  
                self.status_obj = PretestUserCompletion(pretestuser=self.pretestuser, completed_pretest=self.worksheet)
                self.status_obj.save()
                elapsed_time_secs = 0

            #  completion record indicates that user has exceeded the time limit. show results page.
            if elapsed_time_secs > self.worksheet.time_limit * 60: 
                    return redirect('pretests:pretest_done', pk=self.worksheet.id, user=self.pretestuser.id)            

            self.time_remaining = self.worksheet.time_limit*60 - elapsed_time_secs 

            return super(PretestQuestionMixin, self).dispatch(*args, **kwargs)

        except Exception as e:
            messages.error(self.request, 'A problem with the testing page as occurred. System admins have been contacted.', extra_tags='danger')
            
            return redirect('pretests:pretest_home')


        
