# core/views.py
from django.views.generic import FormView, TemplateView, CreateView, UpdateView, ListView, DetailView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail


from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms, remove_perm

from courses.models import Course

from .models import Bookmark, GGVUser, SiteMessage, Notification, SitePage
from .forms import BookmarkForm, GgvUserAccountCreateForm, GgvUserSettingsForm, GgvUserAccountUpdateForm, GgvEmailForm, GgvUserStudentSettingsForm, GgvEmailInstructorsForm
from .mixins import CourseContextMixin, GGVUserViewRestrictedAccessMixin
from .signals import *


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['site_message'] = SiteMessage.objects.get(url_context='/')
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggvhome.html'

    def get(self, request, *args, **kwargs):
        try:
            courses = self.request.session['user_courses']

            if len(courses) == 1:
                return redirect('course', crs_slug=courses[0])
        except:
            courses = None

        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = [
            Course.objects.get(slug=i) for i in self.request.session['user_courses']]

        return context


class CreateGgvUserView(LoginRequiredMixin, CourseContextMixin, CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = GgvUserAccountCreateForm
    course = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
        except:
            self.course = None

        return super(CreateGgvUserView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Return the user back to the add form.
        return reverse('create_user', args=[self.kwargs['crs_slug']])

    def get_initial(self):
        initial = self.initial.copy()
        initial = {
            'course': self.course, 'language': 'english', 'is_active': False, 'perms': 'access'}
        return initial

    def form_valid(self, form):
        self.object = form.save()
        language = form.cleaned_data['language']
        course = form.cleaned_data['course']
        perms = form.cleaned_data['perms']
        prog_id = form.cleaned_data['program_id']
        ggvuser = GGVUser(user=self.object, language_pref=language, program_id=prog_id)
        ggvuser.save()
        assign_perm(perms, self.object, course)

        return super(CreateGgvUserView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateGgvUserView, self).get_context_data(**kwargs)
        student_list = self.course.student_list()
        context['students'] = student_list
        context['instructors'] = self.course.instructor_list()
        # context['unregistered'] = User.objects.filter().filter(social_auth__user__isnull=True)
        # context['deactivated'] = User.objects.filter(social_auth__user__isnull=True)

        return context


class UpdateGgvUserAccountView(LoginRequiredMixin, GGVUserViewRestrictedAccessMixin, CourseContextMixin, UpdateView):
    model = User
    template_name = 'user_account_edit.html'
    form_class = GgvUserAccountUpdateForm
    required_privileges = ['manage']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
            self.ggvuser = GGVUser.objects.get(user=self.get_object())
            self.permissions = get_perms(self.get_object(), self.course)[0]
        except:
            raise Http404(self.get_object().username + ' is not part of ' + self.course.title)

        return super(UpdateGgvUserAccountView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('view_user', args=[self.course.slug, self.get_object().id])

    def get_initial(self):
        initial = self.initial.copy()
        initial = {'course': self.course, 'perms': self.permissions, 'program_id': self.ggvuser.program_id}
        return initial

    def form_valid(self, form):
        self.object = form.save()
        username = form.cleaned_data['username']
        language = form.cleaned_data['language']
        course = form.cleaned_data['course']
        perms = form.cleaned_data['perms']
        prog_id = form.cleaned_data['program_id']

        self.ggvuser.program_id = prog_id
        self.ggvuser.language_pref = language
        self.ggvuser.save()

        curr_permissions = get_perms(self.object, self.course)

        # Username changed?
        if not self.object.email == username:
            self.object.email = username
            self.object.save()

        # Change the user's course?.
        if not self.course.id == course.id:

            for i in curr_permissions:
                assign_perm(i, self.object, course)
                remove_perm(i, self.object, self.course)

            self.course = course

        # Change the user's permissions?
        if perms not in curr_permissions:
            for i in curr_permissions:
                remove_perm(i, self.object, self.course)

            assign_perm(perms, self.object, self.course)

        return super(UpdateGgvUserAccountView, self).form_valid(form)


class GgvUserView(LoginRequiredMixin, GGVUserViewRestrictedAccessMixin, CourseContextMixin, DetailView):
    model = User
    template_name = 'user_view.html'
    required_privileges = ['user', 'manage']

    def get_context_data(self, **kwargs):
        context = super(GgvUserView, self).get_context_data(**kwargs)
        context['ggvuser'] = GGVUser.objects.get(user=self.get_object())
        context['roles'] = get_perms(self.get_object(), context['course'])
        return context


class UpdateGgvUserView(LoginRequiredMixin, GGVUserViewRestrictedAccessMixin, CourseContextMixin, UpdateView):
    model = User
    template_name = "user_edit.html"
    form_class = GgvUserStudentSettingsForm
    success_url = reverse_lazy('ggvhome')
    required_privileges = ['manage']

    def dispatch(self, request, *args, **kwargs):
        if get_objects_for_user(self.get_object(), ['instructor', 'manage'], Course, any_perm=True):
            self.form_class = GgvUserSettingsForm

        self.ggvuser = self.get_object().ggvuser
        return super(UpdateGgvUserView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = self.initial.copy()
        ggvuser = self.get_object().ggvuser

        if self.form_class == GgvUserSettingsForm:
            initial = {'language': ggvuser.language_pref, 'clean_logout': ggvuser.clean_logout, 'receive_notify_email': ggvuser.receive_notify_email, 'receive_email_messages': ggvuser.receive_email_messages}
        else:
            initial = {'language': ggvuser.language_pref, 'clean_logout': ggvuser.clean_logout}
        return initial

    def form_valid(self, form):
        self.object = form.save()
        self.ggvuser.language_pref = form.cleaned_data['language']
        self.ggvuser.clean_logout = form.cleaned_data['clean_logout']
        try:
            self.ggvuser.receive_notify_email = form.cleaned_data['receive_notify_email']
            self.ggvuser.language_pref = form.cleaned_data['receive_email_messages']
        except:
            pass

        self.ggvuser.save()
        return super(UpdateGgvUserView, self).form_valid(form)


class GgvUserActivationView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update_activation.html'
    fields = ['is_active']

    def get_success_url(self):
        try:
            # Hack to return the user back to the course manage list.
            str = self.request.META['HTTP_REFERER']
            str = str[str.find('q=')+2:]
            return reverse('manage_course', args=[str])
        except:
            return reverse('ggvhome')


class ActivateView(LoginRequiredMixin, TemplateView):
    template_name = 'activate.html'


class AccessForbiddenView(CourseContextMixin, TemplateView):
    template_name = 'access_forbidden.html'


class ActivityLogView(TemplateView):
    pass


class SendEmailToInstructorsView(LoginRequiredMixin, CourseContextMixin, FormView):
    form_class = GgvEmailInstructorsForm
    template_name = "ggv_send_email.html"
    success_url = None
    course = None

    def get_success_url(self):
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])

        return super(SendEmailToInstructorsView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_sender = self.request.user.first_name + ' ' + self.request.user.last_name + ' ' + self.request.user.email
        instructor_list = []
        for i in self.course.instructor_list():
            instructor_list.append(i.email)

        message = "Hi {course} Instructors, {sender} has sent you the following message: ".format(
            course=self.course,
            sender=user_sender)

        message += "\n\n{0}".format(form.cleaned_data.get('message'))

        send_mail(
            subject='Message from one of your GGV students',
            message=message,
            from_email='ggvsys@gmail.com',
            recipient_list=instructor_list,
        )

        return super(SendEmailToInstructorsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SendEmailToInstructorsView, self).get_context_data(**kwargs)

        return context

class SendEmailToStaff(LoginRequiredMixin, CourseContextMixin, FormView):
    form_class = GgvEmailInstructorsForm
    template_name = "ggv_send_email.html"
    success_url = None
    course = None

    def get_success_url(self):
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')

    def dispatch(self, request, *args, **kwargs):
        self.course = Course.objects.get(slug=kwargs['crs_slug'])

        return super(SendEmailToInstructorsView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_sender = self.request.user.first_name + ' ' + self.request.user.last_name + ' ' + self.request.user.email
        instructor_list = []
        for i in self.course.instructor_list():
            instructor_list.append(i.email)

        message = "Hi GGV Staff, {sender} has sent you the following message: ".format(sender=user_sender)

        message += "\n\n{0}".format(form.cleaned_data.get('message'))

        send_mail(
            subject='Message from a GGV user',
            message=message,
            from_email='ggvsys@gmail.com',
            recipient_list=['ggvsys@gmail.com', 'drchingon7@gmail.com', 'gedgonevirtual@gmail.com'],
        )

        return super(SendEmailToInstructorsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SendEmailToInstructorsView, self).get_context_data(**kwargs)

        return context


class SendEmailMessageView(LoginRequiredMixin, FormView):
    form_class = GgvEmailForm
    template_name = "ggv_send_email.html"
    success_url = None

    def get_success_url(self):
        try:
            return self.request.GET['q']
        except:
            return reverse('ggvhome')


    def form_valid(self, form):
        message = "Hi {recipient_name}, {senders_name} said: ".format(
            senders_name=form.cleaned_data.get('senders_name'),
            recipient_name=form.cleaned_data.get('recipient_name'))
        message += "\n\n{0}".format(form.cleaned_data.get('message'))
        send_mail(
            subject=form.cleaned_data.get('subject').strip(),
            message=message,
            from_email='ggvsys@gmail.com',
            recipient_list=['ggvsys@gmail.com', form.cleaned_data.get('recipient_email')],
        )

        return super(SendEmailMessageView, self).form_valid(form)


class CreateMessageView(TemplateView):
    pass


class BookmarkAjaxCreateView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Bookmark

    def post_ajax(self, request, *args, **kwargs):
        bookmarkform = BookmarkForm(request.POST)
        data = {}
        try:
            # print bookmarkform
            new_bookmark = bookmarkform.save()

            label = new_bookmark.get_mark_type_display()
            try:
                if 'span' in request.POST['lesson_lang']:
                    label = label.split(',')[1]
                else:
                    label = label.split(',')[0]

                data['mark_type'] = label
            except:
                pass

            data['bookmark_id'] = new_bookmark.id

            for i in new_bookmark.course_context.instructor_list():
                notification = Notification(user_to_notify=i, context='bookmark', event=new_bookmark.notify_text())
                notification.save()

        except Exception as e:
            pass

        return self.render_json_response(data)


class BookmarkAjaxUpdateView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, UpdateView):
    model = Bookmark

    def post_ajax(self, request, *args, **kwargs):
        bookmarkform = BookmarkForm(request.POST)

        try:
            bookmarkform.form_valid()
            data = {}
            updated_bk = self.get_object()
            updated_bk.mark_type = bookmarkform.cleaned_data['mark_type']
            updated_bk.save()

            label = updated_bk.get_mark_type_display()
            if 'span' in request.POST['lesson_lang']:
                label = label.split(',')[1]
            else:
                label = label.split(',')[0]

            data['mark_type'] = label
            data['bookmark_id'] = updated_bk.id

            for i in updated_bk.course_context.instructor_list():
                notification = Notification(user_to_notify=i, context='bookmark', event=updated_bk.notify_text())
                notification.save()

        except Exception:
            pass

        return self.render_json_response(data)


class BookmarkAjaxDeleteView(LoginRequiredMixin, CourseContextMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, UpdateView):
    model = Bookmark

    def post_ajax(self, request, *args, **kwargs):
        bookmarkform = BookmarkForm(request.POST)
        # if bookmarkform.is_valid():
        self.get_object().delete()
        data = {}
        data['deleted'] = 'deleted'
        return self.render_json_response(data)
        # else:

            # data = bookmarkform.errors
            # print data
            # return self.render_json_response(data)


class FaqView(TemplateView):
    template_name = 'faq.html'

    def get_context_data(self, **kwargs):
        context = super(FaqView, self).get_context_data(**kwargs)
        context["sitepage"] = SitePage.objects.get(title='FAQ')
        return context


