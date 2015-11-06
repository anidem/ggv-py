# core/emails.py
from django.views.generic import FormView, TemplateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib import messages
from django.contrib.messages import get_messages
from django.conf import settings

from braces.views import LoginRequiredMixin
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms

from courses.models import Course
from questions.models import QuestionSet

from .models import GGVUser
from .forms import GgvEmailStaffForm, GgvEmailQuestionToInstructorsForm, GgvEmailWorksheetErrorReportToStaffForm, GgvEmailInstructors
from .mixins import CourseContextMixin
from .signals import *


class SendEmailToInstructor(LoginRequiredMixin, CourseContextMixin, FormView):
    """
    A general purpose view to allow a student to email the instructor(s) assigned to the student's course. This view ADHERES
    to the email settings for instructors.
    """
    form_class = GgvEmailInstructors
    template_name = "ggv_send_email.html"
    success_url = None
    course = None

    def get_success_url(self):
        """Attempts to redirect user back to original page if return url is in q"""
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])
        return super(SendEmailToInstructor, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_sender = self.request.user
        instructor_list = []
        for i in self.course.instructor_list():  # Bypassing user settings to control email messages from ggv system
            if i.ggvuser.receive_email_messages:
                instructor_list.append(i.email)

        if not instructor_list:  # Nobody to send to. Recipient list is empty!
            messages.info(self.request, 'Your instructor(s) did not receive your email. They have currently opted to not receive emails from this website. Please let them know that you would like to use this function. You can always email them directly using your preferred email client.')

        else:
            html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=self.request.user.email)
            html_message += "<p>Hi {course} Instructors, {sender} has sent you message: </p>".format(
                course=self.course,
                sender=user_sender)

            html_message += "<h3>{0}</h3>".format(form.cleaned_data.get('message'))

            html_message += "<p><i>You are receiving this email as a courtesy of ggvinteractive.com. You currently have your personal settings set to: <b>Choose to receive email messages from the GGV system.</b>. Please contact your ggvinteractive administrator or ggv representative for information about these emails or turning off email messages from ggv.</i></p>"

            email = EmailMultiAlternatives(
                subject=user_sender.get_full_name() + ' has a message for you',
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=instructor_list,
                headers={'Reply-To': self.request.user.email},  # this can be updated after upgrading to django 8+
                )

            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)
            messages.info(self.request, 'Your message was sent as an email message to your instructors.')

        return super(SendEmailToInstructor, self).form_valid(form)


class SendEmailWorksheetQuestionToInstructorsView(LoginRequiredMixin, CourseContextMixin, FormView):
    """
    A view that sends an email regarding a specific question to instructors assigned to a course. This view is intended to work with
    worksheet views so that students can email a question to instructors regarding a specific worksheet question.
    This view ADHERES to the email_settings for instructors. (e.g., Instructors can choose NOT to receive email from GGV)

    recipients: instructors associated with the course who have allowed email from the system.
    sender: system sends but indicates the current user email in reply-to field.

    use case: Student emails instructor about a worksheet question.
    """
    form_class = GgvEmailQuestionToInstructorsForm
    template_name = "ggv_send_email.html"
    success_url = None
    course = None
    worksheet = None
    question = None

    def get_success_url(self):
        """Attempts to redirect user back original page if return url is in q"""
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])
        self.worksheet = QuestionSet.objects.get(pk=kwargs['i'])
        self.question = kwargs['j']
        return super(SendEmailWorksheetQuestionToInstructorsView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_sender = self.request.user.first_name + ' ' + self.request.user.last_name + ' ' + self.request.user.email
        instructor_list = []
        for i in self.course.instructor_list():  # Bypassing user settings to control email messages from ggv system
            if i.ggvuser.receive_email_messages:
                instructor_list.append(i.email)

        if not instructor_list:  # Nobody to send to. Recipient list is empty!
            messages.info(self.request, 'Your instructor(s) did not receive your email. They have currently opted to not receive emails from this website. Please let them know that you would like to use this function. You can always email them directly using your preferred email client.')

        else:
            html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=self.request.user.email)
            html_message += "<p>Hi {course} Instructors, {sender} has sent you the following message regarding worksheet: </p><p><b>Question no. {quest} in worksheet {ws}</b></p> ".format(
                course=self.course,
                ws=self.worksheet,
                quest=self.question,
                sender=user_sender)

            question_url = 'http://' + request.get_host() + reverse('question_response', args=[self.course.slug, self.worksheet.id, self.question])

            html_message += "<p>Question: <a href=\"{q_url}\">{q_url}</a></p>".format(q_url=question_url)

            html_message += "<h3>{0}</h3>".format(form.cleaned_data.get('message'))

            html_message += "<p><i>You are receiving this email as a courtesy of ggvinteractive.com. You currently have your personal settings set to: <b>Choose to receive email messages from the GGV system.</b>. Please contact your ggvinteractive administrator or ggv representative for information about these emails or turning off email messages from ggv.</i></p>"

            email = EmailMultiAlternatives(
                subject=self.request.user.first_name + ' ' + self.request.user.last_name + ' has a question for you',
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=instructor_list,
                headers={'Reply-To': self.request.user.email},  # this can be updated after upgrading to django 8+
                )

            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)
            messages.info(self.request, 'Your question was sent as an email message to your instructors.')

        return super(SendEmailWorksheetQuestionToInstructorsView, self).form_valid(form)


class SendEmailWorksheetErrorToStaffView(LoginRequiredMixin, CourseContextMixin, FormView):
    """
    A view that allows students/instructors to email an error report regarding a worksheet question.
    This may be an correct answer that is incorrectly assigned to the question or other technical problems viewing
    or responding to the question.

    recipients: ggv staff.
    sender: system sends but indicates the current user email in reply-to field.

    use case: Student or instructor reports an error in a worksheet to GGV Content Developers. (ggv staff)
    """

    form_class = GgvEmailWorksheetErrorReportToStaffForm
    template_name = "ggv_send_email.html"
    success_url = None
    course = None
    worksheet = None
    question = None

    def get_success_url(self):
        """Attempts to redirect user back original page if return url is in q"""
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])
        self.worksheet = QuestionSet.objects.get(pk=kwargs['i'])
        self.question = kwargs['j']
        return super(SendEmailWorksheetErrorToStaffView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=self.request.user.email)
        html_message += "<p>Hi GGV Staff, {sender} (in {course}) is reporting an error in question <b>{quest}</b> in worksheet <b>{ws}</b></p> ".format(
            course=self.course,
            ws=self.worksheet,
            quest=self.question,
            sender=self.request.user.get_full_name())

        question_url = 'http://' + request.get_host() + reverse('question_response', args=[self.course.slug, self.worksheet.id, self.question])

        html_message += "<p>View question: <a href=\"{q_url}\">{q_url}</a></p>".format(q_url=question_url)

        html_message += "<p>{sender}'s message:</p><h3>{msg}</h3>".format(
            sender=self.request.user.get_full_name(),
            msg=form.cleaned_data.get('message'),
            )

        email = EmailMultiAlternatives(
            subject=self.request.user.get_full_name() + ' is reporting a problem in a GGV worksheet',
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[e.email for e in User.objects.filter(is_staff=True).filter(is_active=True)],
            headers={'Reply-To': self.request.user.email},  # this can be updated after upgrading to django 8+
            )

        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)
        messages.info(self.request, 'Thank you for reporting a problem! Your message to GGV Staff has been sent. We\'ll get crackin on it soon.')
        return super(SendEmailWorksheetErrorToStaffView, self).form_valid(form)


class SendEmailToStaff(LoginRequiredMixin, FormView):
    """
    A view to allow users to report an issue, problem, or comment to GGV Staff.

    recipients: GGV Staff
    sender: system sends but indicates the current user email in reply-to field.
    scope: global
    """
    form_class = GgvEmailStaffForm
    template_name = "ggv_send_email.html"
    success_url = None

    def get_success_url(self):
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')

    def form_valid(self, form):
        user_sender = self.request.user
        course_slugs = self.request.session['user_courses']
        course_titles = ''
        for i in course_slugs:
            course_titles += Course.objects.get(slug=i).title + ', '

        html_message = "<p>Hi GGV Staff, {sender} has sent you the following message:</p> ".format(sender=user_sender.get_full_name())

        html_message += "<h3>{0}</h3>".format(form.cleaned_data.get('message'))

        html_message += '<p>User Info:</p><p>Email: <b>{email}</b></p><p>Member of: <b>{courses}</b></p>'.format(email=user_sender.email, courses=course_titles)

        email = EmailMultiAlternatives(
            subject=self.request.user.get_full_name() + ' has a message about GGV',
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[e.email for e in User.objects.filter(is_staff=True).filter(is_active=True)],
            headers={'Reply-To': user_sender.email},  # this can be updated after upgrading to django 8+
            )

        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)

        return super(SendEmailToStaff, self).form_valid(form)


# BACKEND EMAIL PROCEDURES. FUNCTIONS THAT ARE INITIATED AUTOMATICALLY BY THE SYSTEM. #


def SendWorksheetNotificationEmailToInstructors(request=None, course=None, worksheet=None):
    """
    A utility method that automatically sends an email to instructors assigned to a course when
    a student has completed a worksheet. Note, this may be critical if instructors have set
    restrictions on when students can view the results of their worksheet responses. Instructors need
    to be aware of worksheet completions in order to decide whether to lift viewing restrictions.
    This view adheres to the email notification settings of each instructor.

    recipients: instructors associated with the course who have email_notifications ON
    sender: system sends but indicates the current user email in reply-to field.

    use case: System emails instructor when a student completes a quiz.
    """
    user_sender = request.user.first_name + ' ' + request.user.last_name + ' (' + request.user.email + ')'
    instructor_list = []
    for i in course.instructor_list():
        if i.ggvuser.receive_notify_email:
            instructor_list.append(i.email)

    worksheet_results_url = 'http://' + request.get_host() + reverse('worksheet_user_report', args=[course.slug, worksheet.id, request.user.id])

    html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=request.user.email)

    html_message += "<p>Hi {crs} Instructors,</p><p> {sndr} has completed the following worksheet:</p>".format(
        crs=course,
        sndr=user_sender)

    html_message += "<p>{ws_lesson} - {ws_title}</p>".format(
        ws_lesson=worksheet.lesson,
        ws_title=worksheet.title,
        )

    html_message += "<p>You can view their responses here:</p><p> <a href=\"{ws_url}\">{ws_url}</a></p><p>Also note you may need to Allow students to view results if you are currently restricting this.</p>".format(
        ws_url=worksheet_results_url,
        )

    html_message += "<p><i>You are receiving this email as a courtesy of ggvinteractive.com. You currently have your personal settings set to: <b>Choose to receive notifications on student activity</b>. Please contact your ggvinteractive administrator or ggv representative for information about these emails or turning off notifications of students worksheet activity.</i></p>"

    email = EmailMultiAlternatives(
        subject=request.user.first_name + ' ' + request.user.last_name + ' has completed a worksheet',
        body=html_message,
        from_email='ggvsys@gmail.com',
        to=instructor_list,
        headers={'Reply-To': request.user.email},  # this can be updated after upgrading to django 8+
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=True)
