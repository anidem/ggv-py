# core/views.py
import json
from pytz import timezone

from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


from braces.views import CsrfExemptMixin, JSONResponseMixin, JsonRequestResponseMixin, AjaxResponseMixin, LoginRequiredMixin
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms, remove_perm

from courses.models import Course

from .models import Bookmark, GGVUser, SiteMessage, Notification, SitePage, AttendanceTracker
from .forms import BookmarkForm, GgvUserAccountCreateForm, GgvUserSettingsForm, GgvUserAccountUpdateForm, GgvUserStudentSettingsForm, GgvEmailQuestionToInstructorsForm, AttendanceTrackerUpdateForm, AttendanceTrackerCreateForm
from .mixins import CourseContextMixin, GGVUserViewRestrictedAccessMixin
from .signals import *

tz = timezone(settings.TIME_ZONE)



class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['site_message'] = SiteMessage.objects.get(url_context='/')
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggvhome.html'
    orgs = []
    courses = None

    def get(self, request, *args, **kwargs):
        try:
            self.courses = self.request.session['user_courses']

            if len(self.courses) == 1:
                return redirect('course', crs_slug=self.courses[0])

            for i in self.courses:
                crs = Course.objects.get(slug=i)
                if crs.ggv_organization not in self.orgs:
                    self.orgs.append(crs.ggv_organization)
        except:
            courses = None

        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = []

        organizations = {}
        
        for o in self.orgs:      
            total_active = 0
            total_deactive = 0
            total_nologin = 0
            course_rows = []

            for course in o.organization_courses.all():

                if self.request.user.has_perm('courses.instructor', course) or self.request.user.has_perm('courses.manage', course) or self.request.user.is_staff :
                    num_active = len(course.student_list())
                    num_deactive = len(course.deactivated_list())
                    num_nologin = len(course.unvalidated_list())

                    total_active = total_active + num_active
                    total_deactive = total_deactive + num_deactive
                    total_nologin = total_nologin + num_nologin

                    crs_data = (
                        course,
                        num_active,
                        num_deactive,
                        num_nologin                
                    )
                    course_rows.append(crs_data)

            organizations[o] = (course_rows, total_active, total_deactive, total_nologin)
        
        context['courses'] = organizations
        # context['total_active'] = total_active
        # context['total_deactive'] = total_deactive
        # context['total_nologin'] = total_nologin

        return context


""" GGVUser Management """
"""TODO!!
create a view to update registration information. For example, to modify the username email, or change the course, etc.
"""



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

        # Need to force lower case emails.
        self.object.username = self.object.username.lower()
        self.object.save()

        # Gather GGVUser object related data.
        language = form.cleaned_data['language']
        course = form.cleaned_data['course']
        perms = form.cleaned_data['perms']
        prog_id = form.cleaned_data['program_id']

        # Make a GGVUser object linked to the User account then assign permissions to the course they are being added to.
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

        # Need to force lower case emails.
        self.object.username = self.object.username.lower()
        self.object.save()

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
    required_privileges = ['access', 'instructor', 'manage']

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
            self.ggvuser.receive_email_messages = form.cleaned_data['receive_email_messages']
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


class GgvUsersDeactivationView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, View):
    
    def post(self, request, *args, **kwargs):
        try:   
            deactivate_list = request.POST.getlist('deactivate_list')   
            urlstr = request.GET['q']
            for i in deactivate_list:
                u = User.objects.get(pk=i)
                u.is_active = False
                u.save()
        except:
            pass  # silently fail

        return redirect('manage_course', crs_slug=urlstr)


class GgvUsersActivationView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, View):
    
    def post(self, request, *args, **kwargs):
        try:   
            activate_list = request.POST.getlist('activate_list')   
            urlstr = request.GET['q']
            for i in activate_list:
                u = User.objects.get(pk=i)
                u.is_active = True
                u.save()
        except:
            pass  # silently fail

        return redirect('manage_course', crs_slug=urlstr)


class ActivateView(LoginRequiredMixin, TemplateView):
    template_name = 'activate.html'


""" Access Forbidden Page """

class AccessForbiddenView(CourseContextMixin, TemplateView):
    template_name = 'access_forbidden.html'


""" Activity Log Page """

class ActivityLogView(TemplateView):
    pass


""" Attendance Tracker Management """

class AttendanceAjaxCodeCreateView(LoginRequiredMixin, JSONResponseMixin, CreateView):
    model = AttendanceTracker
    require_json = True

    def post(self, request, *args, **kwargs):
        trackerform = AttendanceTrackerCreateForm(request.POST)

        try:
            trackerform.form_valid()

            datestr_obj = trackerform.cleaned_data['datestamp'].astimezone(tz).strftime('%Y-%m-%d')

            data = {}
            new_tracker = AttendanceTracker(
                user=trackerform.cleaned_data['user'],
                datestamp=trackerform.cleaned_data['datestamp'],
                datestr=datestr_obj,
                code=trackerform.cleaned_data['code']
                )
            
            new_tracker.save()

            data['added'] = 'added'
            data['code'] = new_tracker.code
            data['code_label'] = new_tracker.get_code_display()
            data['attendance_id'] = new_tracker.id

        except Exception as e:
            pass

        return self.render_json_response(data)


class AttendanceAjaxCodeUpdateView(LoginRequiredMixin, JSONResponseMixin, UpdateView):
    model = AttendanceTracker
    require_json = True

    def post(self, request, *args, **kwargs):
        trackerform = AttendanceTrackerUpdateForm(request.POST)

        try:
            trackerform.form_valid()
            data = {}
            updated_att = self.get_object()
            updated_att.code = trackerform.cleaned_data['code']
            updated_att.save()

            data['code'] = updated_att.code
            data['code_label'] = updated_att.get_code_display()
            data['attendance_id'] = updated_att.id

        except Exception as e:
            pass

        return self.render_json_response(data) 


class AttendanceAjaxCodeDeleteView(LoginRequiredMixin, JSONResponseMixin, DeleteView):
    model = AttendanceTracker

    def post(self, request, *args, **kwargs):
        try:
            data = {}

            self.get_object().delete()

            data['deleted'] = 'deleted'
            data['code'] = ''

        except Exception as e:
            pass

        return self.render_json_response(data) 


""" Bookmark Management """

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


""" Frequently Asked Questions Page """

class FaqView(TemplateView):
    template_name = 'faq.html'

    def get_context_data(self, **kwargs):
        context = super(FaqView, self).get_context_data(**kwargs)
        context["sitepage"] = SitePage.objects.get(title='FAQ')
        return context


""" Error Pages """

def handler404(request):
    response = render_to_response('404_custom_error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('500_custom_error.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response



