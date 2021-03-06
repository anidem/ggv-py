# This Python file uses the following encoding: utf-8
# core/emails.py

from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib import messages
from django.contrib.messages import get_messages
from django.conf import settings

from braces.views import LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms

from courses.models import Course
from questions.models import QuestionSet

from .models import GGVUser
from .forms import GgvEmailStaffForm, GgvEmailQuestionToInstructorsForm, GgvEmailWorksheetErrorReportToStaffForm, GgvEmailInstructors, GgvEmailDeactivationRequestForm, GgvEmailActivationRequestForm, GgvUserAccountCreateForm, GgvEmailManagerRequestAccountForm
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
            messages.info(self.request, 'Your instructor(s) did not receive your email but other administrative staff will be contacted.')

            for i in self.course.manager_list():
                instructor_list.append(i.email)

        else:
            html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=self.request.user.email)
            html_message += "<p>Hi {course} Instructors, {sender} has sent you message: </p>".format(
                course=self.course,
                sender=user_sender)

            message_text = form.cleaned_data.get('message').encode('utf-8')
            html_message += "<h3>{0}</h3>".format(message_text)

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
            messages.info(self.request, 'Your instructor(s) did not receive your email but other administrative staff will be contacted.')

            for i in self.course.manager_list():
                instructor_list.append(i.email)

        else:
            html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=self.request.user.email)
            html_message += "<p>Hi {course} Instructors, {sender} has sent you the following message regarding worksheet: </p><p><b>Question no. {quest} in worksheet {ws}</b></p> ".format(
                course=self.course,
                ws=self.worksheet,
                quest=self.question,
                sender=user_sender)

            question_url = 'http://' + self.request.get_host() + reverse('question_response', args=[self.course.slug, self.worksheet.id, self.question])

            html_message += "<p>Question: <a href=\"{q_url}\">{q_url}</a></p>".format(q_url=question_url)

            message_text = form.cleaned_data.get('message').encode('utf-8')
            html_message += "<h3>{0}</h3>".format(message_text)

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

        question_url = 'http://' + self.request.get_host() + reverse('question_response', args=[self.course.slug, self.worksheet.id, self.question])

        html_message += "<p>View question: <a href=\"{q_url}\">{q_url}</a></p>".format(q_url=question_url)

        message_text = form.cleaned_data.get('message').encode('utf-8')

        html_message += "<p>{sender}'s message:</p><h3>{msg}</h3>".format(
            sender=self.request.user.get_full_name(),
            msg=message_text,
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
        messages.info(self.request, 'Thank you for reporting a problem! Your message to GGV Staff has been sent. We\'ll get crackin on it soon.  Please check your email soon for an update on the problem. ')
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

        message_text = form.cleaned_data.get('message').encode('utf-8')
        html_message += "<h3>{0}</h3>".format(message_text)

        html_message += '<p>Sender Info:</p><p>Email: <b>{email}</b></p><p>Member of: <b>{courses}</b></p>'.format(email=user_sender.email, courses=course_titles)

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


class SendEmailToManagerDeactivationRequest(CsrfExemptMixin, LoginRequiredMixin, CourseContextMixin, JSONResponseMixin, View):
    course = None

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])
        return super(SendEmailToManagerDeactivationRequest, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:   
            deactivate_list = request.POST.getlist('deactivate_list')   
            urlstr = request.GET['q']
            users = ''
            for i in deactivate_list:
                u = User.objects.get(pk=i)
                users = users + u.ggvuser.program_id + ' ' + u.first_name + ' ' + u.last_name + ' (' + u.email + '),  '

            user_sender = self.request.user

            user_org = self.course.ggv_organization

            url_org =  'http://' + self.request.get_host() + reverse('manage_org', args=[user_org.id])

            manager_list = []
            for i in self.course.manager_list():  # Bypassing user settings to control email messages from ggv system
                manager_list.append(i.email)
   
            if not manager_list: # if not manager found. send request to staff.
                staff = User.objects.filter(is_staff=True)
                for i in staff:
                    manager_list.append(i.email)

            course_slugs = self.request.session['user_courses']
            course_titles = ''
            for i in course_slugs:
                course_titles += Course.objects.get(slug=i).title + ', '

            html_message = "<p>Hi GGV Site Manager, {sender} has sent you the following message:</p> ".format(sender=user_sender.get_full_name())

            html_message += "<h3>Please deactivate the following accounts.</h3> <p>{0}</p>".format(users)

            html_message += '<p>Requestor Info::</p><p>Email: <b>{email}</b></p><p>Member of: <b>{courses}</b></p>'.format(email=user_sender.email, courses=course_titles)

            html_message += '<p>Manage deactivations here ==> <a href=\"{org_url}\">{org}</a></p>'.format(org_url=url_org, org=user_org)

            email = EmailMultiAlternatives(
                subject=self.request.user.get_full_name() + ' is requesting deactivation for users.',
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=manager_list,
                headers={'Reply-To': user_sender.email},  # this can be updated after upgrading to django 8+
                )
            
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)
            messages.info(self.request, 'Your request to deactivate ' + users + ' has been sent to ' + ', '.join(manager_list))
               
        except Exception as e:
            print e
            pass  # silently fail

        return redirect('manage_course', crs_slug=urlstr)


class SendEmailToManagerActivationRequest(CsrfExemptMixin, LoginRequiredMixin, CourseContextMixin, JSONResponseMixin, View):
    course = None

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])
        return super(SendEmailToManagerActivationRequest, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:   
            activate_list = request.POST.getlist('activate_list')   
            urlstr = request.GET['q']
            users = ''
            for i in activate_list:
                u = User.objects.get(pk=i)
                users = users + u.ggvuser.program_id + ' ' + u.first_name + ' ' + u.last_name + ' (' + u.email + '),  '

            user_sender = self.request.user

            user_org = self.course.ggv_organization

            url_org =  'http://' + self.request.get_host() + reverse('manage_org', args=[user_org.id])

            manager_list = []
            for i in self.course.manager_list():  # Bypassing user settings to control email messages from ggv system
                manager_list.append(i.email)
   
            if not manager_list: # if not manager found. send request to staff.
                staff = User.objects.filter(is_staff=True)
                for i in staff:
                    manager_list.append(i.email)
                    
            course_slugs = self.request.session['user_courses']
            course_titles = ''
            for i in course_slugs:
                course_titles += Course.objects.get(slug=i).title + ', '

            html_message = "<p>Hi GGV Site Manager, {sender} has sent you the following message:</p> ".format(sender=user_sender.get_full_name())

            html_message += "<h3>Please activate the following accounts.</h3> <p>{0}</p>".format(users)

            html_message += '<p>Requestor Info:</p><p>Email: <b>{email}</b></p><p>Member of: <b>{courses}</b></p>'.format(email=user_sender.email, courses=course_titles)

            html_message += '<p>Manage activations here ==> <a href=\"{org_url}\">{org}</a></p>'.format(org_url=url_org, org=user_org)

            email = EmailMultiAlternatives(
                subject=self.request.user.get_full_name() + ' is requesting activation for users.',
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=manager_list,
                headers={'Reply-To': user_sender.email},  # this can be updated after upgrading to django 8+
                )

            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=True)
            messages.info(self.request, 'Your request to activate '+ users + ' has been sent to ' + ', '.join(manager_list))

        except Exception as e:
            print e
            pass  # silently fail

        return redirect('manage_course', crs_slug=urlstr)


class SendEmailToManagerCreateAccountRequest(LoginRequiredMixin, CourseContextMixin, FormView):
    """
    A view to allow instructors to send a new account request to managers of a ggv organization.

    recipients: GGV Organization Manager
    sender: system sends but indicates the current user email in reply-to field.
    scope: global
    """
    form_class = GgvEmailManagerRequestAccountForm
    template_name = "ggv_send_account_request.html"
    success_url = None
    course = None

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])
        return super(SendEmailToManagerCreateAccountRequest, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('course', args=[self.course.slug])

    def form_valid(self, form):
        user_sender = self.request.user
        perm = form.cleaned_data.get('perms')
        if perm == 'access':
            perm = 'student'

        recipients = [i.email for i in self.course.manager_list()]
        if not recipients:
            recipients = [e.email for e in User.objects.filter(is_staff=True).filter(is_active=True)]

        html_message = "<p>Hi, {sender} is requesting a new account on behalf of the person indicated below.</p> ".format(sender=user_sender.get_full_name())

        html_message += "<h3>New user:</h3>"
        html_message += "<p>Username (email): {0}</p>".format(form.cleaned_data.get('username'))
        html_message += "<p>First Name: {0}</p>".format(form.cleaned_data.get('first_name'))
        html_message += "<p>Last Name: {0}</p>".format(form.cleaned_data.get('last_name'))
        html_message += "<p>Access Level: {0}</p>".format(perm)
        html_message += "<p>Progam ID: {0}</p>".format(form.cleaned_data.get('program_id'))
        html_message += "<p>Language: {0}</p>".format(form.cleaned_data.get('language'))
        html_message += "<p>Course: {0}</p>".format(self.course)

        email = EmailMultiAlternatives(
            subject=self.request.user.get_full_name() + ' is requesting a new account',
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients,
            headers={'Reply-To': user_sender.email},  # this can be updated after upgrading to django 8+
            )

        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)
        messages.info(self.request, 'Your request for a new account has been sent to the managers for your account.')
        return super(SendEmailToManagerCreateAccountRequest, self).form_valid(form)



""" BACKEND EMAIL PROCEDURES. FUNCTIONS THAT ARE INITIATED AUTOMATICALLY BY THE SYSTEM. """

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
    # print user_sender
    # user_sender = user_sender.decode('utf-8')

    gedid = ''
    if request.user.ggvuser.program_id:
        gedid = request.user.ggvuser.program_id

    instructor_list = []
    for i in course.instructor_list():
        if i.ggvuser.receive_notify_email:
            instructor_list.append(i.email)

    if not instructor_list:  # Nobody to send to. Recipient list is empty!
        messages.info(self.request, 'Your instructor(s) did not receive your email but other administrative staff will be contacted.')

        for i in course.manager_list():
            instructor_list.append(i.email)

    worksheet_results_url = 'http://' + request.get_host() + reverse('worksheet_user_report', args=[course.slug, worksheet.id, request.user.id])

    html_message = "<p><b>Replies to this message will be sent to: {usr_email}</b></p>".format(usr_email=request.user.email)

    try:

        html_message += "<p>Hi {crs} Instructors,</p><p> {sndr} has completed the following worksheet:</p>".format(
            crs=course,
            sndr=user_sender)

        html_message += "<p>{ws_lesson} - {ws_title}</p>".format(
            ws_lesson=worksheet.lesson,
            ws_title=worksheet)

    except Exception as e:
        # print html_message, e
        pass

    html_message += "<p>You can view their responses here:</p><p><a href=\"{ws_url}\">{ws_url}</a><b>Login required.</b></p><p>Also note you may need to Allow students to view results if you are currently restricting this.</p>".format(
        ws_url=worksheet_results_url,
        )

    html_message += "<p><i>You are receiving this email as a courtesy of ggvinteractive.com. You currently have your personal settings set to: <b>Choose to receive notifications on student activity</b>. Please contact your ggvinteractive administrator or ggv representative for information about these emails or turning off notifications of students worksheet activity.</i></p>"

    email = EmailMultiAlternatives(
        subject=str(gedid) + ' - ' + request.user.first_name + ' ' + request.user.last_name + ' in ' + course.title + ' has completed a worksheet',
        body=html_message,
        from_email='ggvsys@gmail.com',
        to=instructor_list,
        headers={'Reply-To': request.user.email},  # this can be updated after upgrading to django 8+
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=True)



def send_request_to_grade(request, course=None, question_response_obj=None):
    """Sends email to official grader (user pk reads from settings file) to
    grade a written response to a pretest.
    """
    if not question_response_obj:
        return

    # if question_response_obj.grade_request_sent:
    #     return

    
    access_url = reverse('question_response_grade', args=[question_response_obj.id])
    access_url = 'http://' + request.get_host() + access_url

    try:
        graders = [i.grader.email for i in course.assigned_graders.all()]
    except:
        return 
    
    msg = 'A GGV Curriculum student (<strong>{0} {1}</strong>) is making a grade request.'.format(question_response_obj.user.first_name, question_response_obj.user.last_name)
    html_message = '<p>' + msg + '</p>'
    html_message += '<p>Course: {0}</p>'.format(course)
    html_message += "<p><a href='{0}'>{0}</a></p>".format(access_url)
    html_message += "<p>{0}</p>".format(question_response_obj.get_question_object())

    email = EmailMultiAlternatives(
        subject='GGV Curriculum - Request to Grade',
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=graders,
        )

    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=True)
    #  not sure about maintaining this status.
    # question_response_obj.grade_request_sent = True
    # question_response_obj.save()
    messages.info(request, 'Your writing response will be graded and scored. Please check back in 48 hours. (Su respuesta de escritura será calificada. Por favor, verifique en 48 horas.)' )
    return