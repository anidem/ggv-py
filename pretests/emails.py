# This Python file uses the following encoding: utf-8
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
from .models import PretestUser, PretestUserCompletion

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
    """Sends email to official grader (user pk reads from settings file) to
    grade a written response to a pretest.
    """
    if not pretest_response_obj:
        return

    if pretest_response_obj.grade_request_sent:
        return

    access_url = reverse('pretests:pretest_response_grade', args=[pretest_response_obj.id], current_app=request.resolver_match.namespace)
    access_url = 'http://' + request.get_host() + access_url

    grader = User.objects.get(pk=settings.GRADER_ID)
    
    msg = 'A GGV pretester is making a grade request.'
    html_message = '<p>' + msg + '</p>'
    html_message += "<p><a href='{0}'>{0}</a></p>".format(access_url)
    html_message += "<p>{0}</p>".format(pretest_response_obj.get_question_object())

    email = EmailMultiAlternatives(
        subject='GGV Pretest - Request to Grade',
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[grader.email,],
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=True)
    pretest_response_obj.grade_request_sent = True
    pretest_response_obj.save()
    messages.info(request, 'Your writing response will be graded and scored. Please check back in 48 hours. (Su respuesta de escritura será calificada. Por favor, verifique en 48 horas.)' )
    return


def send_completion_notification(request, pretest_completion_obj=None):
    # EMAILS MANAGER
    if not pretest_completion_obj:
        return

    if pretest_completion_obj.notification_sent:
        return 

    access_url = reverse('pretests:pretest_user_detail', args=[pretest_completion_obj.pretestuser.id], current_app=request.resolver_match.namespace)
    access_url = 'http://' + request.get_host() + access_url

    pretest = pretest_completion_obj.completed_pretest
    pretester = pretest_completion_obj.pretestuser.first_name + ' ' + pretest_completion_obj.pretestuser.last_name
    pretest_account = pretest_completion_obj.pretestuser.account
 
    html_message = '<p>{0} has completed a pretest: <strong>{1}</strong></p>'.format(pretester, pretest)
    html_message += "<p>View results here:<a href='{0}'>{0}</a></p>".format(access_url)
    html_message += '<h4>Pretest User Info:</h4>'
    html_message += '<p>Name: {0}</p>'.format(pretester)
    html_message += '<p>Access Token: {0}</p>'.format(pretest_completion_obj.pretestuser.access_token)

    if pretest_account.ggv_org:
        html_message += '<p>GGV Interactive Account: {0}</p>'.format(pretest_account.ggv_org)
        html_message += '<p>GGV Interactive Program ID: {0}</p>'.format(pretest_completion_obj.pretestuser.program_id)
          
    email = EmailMultiAlternatives(
        subject=pretester + ' has completed a pretest',
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[pretest_account.manager.email],
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
    pretest_completion_obj.notification_sent = True
    pretest_completion_obj.save()
    return

def send_score_notification(request, pretest_response_obj=None):
    """Sends two emails:
    a) to pretest user that a written response has been graded.
    b) to pretest account manager (associated with pretest user)
    that assessment of the current pretest exam has been completed.
    """
    if not pretest_response_obj:
        return

    access_url = reverse('pretests:pretest_home', current_app=request.resolver_match.namespace)
    access_url = 'http://' + request.get_host() + access_url

    pretest = pretest_response_obj.content_object.question_set
    pretester = pretest_response_obj.pretestuser.first_name + ' ' + pretest_response_obj.pretestuser.last_name
    pretest_account =  pretest_response_obj.pretestuser.account
    score = pretest_response_obj.score
    if score > 0: score = 'PASSED'
    else: score = 'DID NOT PASS'

    msg = ' .'
    html_message = '<p>Hi {1},</p><p>Your written response to {0} has been graded.</p>'.format(pretest, pretester)
    html_message += '<p>Your written response <strong>{0}</strong>.'.format(score)
    html_message += "<p>Click link to see your assessed score:<a href='{0}'>{0}</a></p>".format(access_url)
   
    email = EmailMultiAlternatives(
        subject=pretester + ' - GGV Pretest Written Response Has Been Graded',
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[pretest_response_obj.pretestuser.email],
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
    messages.info(request, 'Pretest user has been emailed at ' + pretest_response_obj.pretestuser.email + '.')

    # SEND EMAIL TO MANAGER
    try:
        pretest_completion_obj = PretestUserCompletion.objects.filter(pretestuser=pretest_response_obj.pretestuser).get(completed_pretest=pretest)
        send_completion_notification(request, pretest_completion_obj)
    except Exception as e:
        pass        

    return

