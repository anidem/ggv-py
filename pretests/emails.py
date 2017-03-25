# emails.py
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import DetailView
from django.conf import settings

from braces.views import LoginRequiredMixin

from .mixins import PretestAccountRequiredMixin
from .models import PretestUser

"""PRETEST EMAIL PROCEDURES"""
class SendPretestTokenView(LoginRequiredMixin, PretestAccountRequiredMixin, DetailView):
    model = PretestUser
    template_name = 'pretest_user_list.html'
    pretest_accounts = None
    access_model = PretestUser

    def dispatch(self, request, *args, **kwargs):
        access_url = reverse('pretests:pretest_home_shortcut',args=[self.get_object().access_token,], current_app=self.request.resolver_match.namespace)
        access_url = 'http://' + request.get_host() + access_url

        html_message = ''
        html_message += "<h2>Hi, you have been granted access to the GGV Pretest System for the GED. Please use the following information to access your exams.</h2>"
        html_message += "<h1>Quick Access:</h1><h2><a href='{0}'>{0}</a></h2>".format(access_url, self.get_object().access_token)
        html_message += "<h1>EMAIL: {0}</h1>".format(self.get_object().email)
        html_message += "<h1>TOKEN: {0}</h1>".format(self.get_object().access_token)
        html_message += "<p>Please email {0} with any questions. </p>".format(self.request.user.email)

        email = EmailMultiAlternatives(
            subject='GGV Interactive Pretest Information',
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.get_object().email,],
            headers={'Reply-To': self.request.user.email},
            )

        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)
        messages.info(self.request, 'Email has been sent to  ' + str(self.get_object().email))        
        return redirect('pretests:pretest_user_list', pk=self.get_object().account.id)



def send_request_to_grade(request, pretest_response_obj=None):

    if not pretest_response_obj:
        return

    access_url = reverse('pretests:pretest_response_grade', args=[pretest_response_obj.id], current_app=request.resolver_match.namespace)
    access_url = 'http://' + request.get_host() + access_url

    grader = User.objects.get(pk=1)
    
    msg = 'A pretester is making a grade request.'
    html_message = '<h2>' + msg + '</h2>'
    html_message += "<h2><a href='{0}'>{0}</a></h2>".format(access_url)
    html_message += "<h2>{0}</h2>".format(pretest_response_obj.get_question_object())

    email = EmailMultiAlternatives(
        subject='GGV Pretest - Request to Grade',
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[grader.email,],
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=True)
    messages.info(request, 'Your writing response will be graded and scored. Please check back in 48 hours.')
    return


def send_score_notification(request, pretest_response_obj=None):

    if not pretest_response_obj:
        return

    access_url = reverse('pretests:pretest_home', current_app=request.resolver_match.namespace)
    access_url = 'http://' + request.get_host() + access_url

    pretest = pretest_response_obj.content_object.question_set

    msg = ' .'
    html_message = '<h2>Your written response to {0} has been graded.</h2>'.format(pretest)
    html_message += "<h2>Click here to see your assessed score:<a href='{0}'>{0}</a></h2>".format(access_url)
    
    email = EmailMultiAlternatives(
        subject='GGV Pretest Question Has Been Graded',
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[pretest_response_obj.pretestuser.email,],
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
    messages.info(request, 'Pretest user has been emailed at ' + pretest_response_obj.pretestuser.email + '.')
    return