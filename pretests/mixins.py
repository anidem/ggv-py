# pretests/mixins.py

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from questions.models import QuestionSet
from .models import PretestUser

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


            return super(PretestQuestionMixin, self).dispatch(*args, **kwargs)

        except Exception as e:
            messages.error(self.request, 'A problem with the testing page as occurred. System admins have been contacted.', extra_tags='danger')
            return redirect('pretests:pretest_home')


        
