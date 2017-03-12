# emails.py
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect
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
        html_message = ''
        html_message += "<h3>Hi, you have been granted access to the GGV Pretest System for the GED. Please use the following information to access your exams.</h3>"
        html_message += "<p>Please go to <a href='{0}'>{0}</a> and enter the following information to begin. Good luck!</p>".format('http://www.ggvinteractive.com/pretest/')
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




