# core/views.py
import json
from pytz import timezone

from django import utils
from django.db import IntegrityError
from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from braces.views import CsrfExemptMixin, JSONResponseMixin, JsonRequestResponseMixin, AjaxResponseMixin, LoginRequiredMixin
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm, get_objects_for_user, get_perms, get_user_perms, remove_perm
from social.exceptions import SocialAuthBaseException, AuthException, AuthForbidden

from courses.models import Course, GGVOrganization
from archiver import serialize_user_data

from .models import Bookmark, GGVUser, SiteMessage, Notification, SitePage, AttendanceTracker
from .forms import BookmarkForm, GgvUserAccountCreateForm, GgvUserSettingsForm, GgvUserAccountUpdateForm, GgvUserStudentSettingsForm, GgvEmailQuestionToInstructorsForm, AttendanceTrackerUpdateForm, AttendanceTrackerCreateForm
from .mixins import CourseContextMixin, GGVUserViewRestrictedAccessMixin
from .signals import *
from .utils import update_attendance_for_all_users

tz = timezone(settings.TIME_ZONE)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['site_message'] = SiteMessage.objects.get(url_context='/')
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'ggvhome.html'
    courses = None

    def get(self, request, *args, **kwargs):
        try:
            self.courses = self.request.session['user_courses']

            if len(self.courses) == 1:
                return redirect('course', crs_slug=self.courses[0])

        except:
            pass

        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = []
        # build organization list from user's course list

        orgs = []
        for i in self.courses:
            crs = Course.objects.get(slug=i)
            if crs.ggv_organization not in orgs:
                orgs.append(crs.ggv_organization)

        organizations = {}
        permissions = []
        for o in orgs:      
            total_active = 0
            total_deactive = 0
            total_nologin = 0
            course_rows = []

            for course in o.organization_courses.all():
                permissions += course.manager_list()
                if  self.request.user.has_perm('courses.manage', course) or self.request.user.is_staff :
                    context['roles'] = ['manage']
                    num_instructors = len(course.instructor_list())
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
                        num_nologin,
                        num_instructors                
                    )
                    course_rows.append(crs_data)
                
                elif self.request.user.has_perm('courses.instructor', course):
                    crs_data = (course,)
                    course_rows.append(crs_data)                    
            
            total_quota_used = len(o.licenses_in_use())

            organizations[o] = (course_rows, total_active, total_deactive, total_nologin, total_quota_used)
        
        context['courses'] = organizations
        context['managers'] = permissions
       
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
        self.course = get_object_or_404(Course, slug=kwargs['crs_slug'])
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
        self.object.email = self.object.username
        self.object.save()

        # Gather GGVUser object related data.
        language = form.cleaned_data['language']
        course = form.cleaned_data['course']
        perms = form.cleaned_data['perms']
        prog_id = form.cleaned_data['program_id']
        if not prog_id:
            prog_id = 'GGV'+str(self.object.id)

        # Make a GGVUser object linked to the User account then assign permissions to the course they are being added to.
        ggvuser = GGVUser(user=self.object, language_pref=language, program_id=prog_id)
        ggvuser.save()
        assign_perm(perms, self.object, course)
        messages.success(self.request, 'User successfully added.')
        return super(CreateGgvUserView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateGgvUserView, self).get_context_data(**kwargs)
        student_list = self.course.student_list()
        context['students'] = student_list
        context['instructors'] = self.course.instructor_list()
        
        user_licenses_used = self.course.ggv_organization.licenses_in_use()
        context['active'] = user_licenses_used['active']
        context['unvalidated'] = user_licenses_used['unvalidated']
        context['license_count'] = user_licenses_used['count']
        # context['licenses'] = user_licenses_used
        context['license_quota'] = self.course.ggv_organization.user_quota
        context['org_courses'] = self.course.ggv_organization.organization_courses.all().exclude(pk=self.course.id)

        # context['unregistered'] = User.objects.filter().filter(social_auth__user__isnull=True)
        # context['deactivated'] = User.objects.filter(social_auth__user__isnull=True)

        return context


class GgvUserView(LoginRequiredMixin, GGVUserViewRestrictedAccessMixin, CourseContextMixin, DetailView):
    model = User
    template_name = 'user_view.html'
    required_privileges = ['user', 'manage']

    def get_context_data(self, **kwargs):
        context = super(GgvUserView, self).get_context_data(**kwargs)
        context['ggvuser'] = GGVUser.objects.get(user=self.get_object())
        context['ggvroles'] = get_user_perms(self.get_object(), context['course'])
        
        return context


class UpdateGgvUserAccountView(LoginRequiredMixin, GGVUserViewRestrictedAccessMixin, CourseContextMixin, UpdateView):
    """
    Edits account information for a user.

    Visibility: System admins, Staff, Managers
    """
    model = User
    template_name = 'user_account_edit.html'
    form_class = GgvUserAccountUpdateForm
    required_privileges = ['manage']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
            self.ggvuser = GGVUser.objects.get(user=self.get_object())
            self.permissions = get_perms(self.get_object(), self.course)
            if not self.permissions:
                # Needed to handle state when user has never logged in. (correct registration information)
                self.permissions = get_user_perms(self.get_object(), self.course)
            self.permissions = self.permissions[0]

        except:
            raise Http404(self.get_object().username + ' is not part of ' + self.course.title)

        return super(UpdateGgvUserAccountView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('view_user', args=[self.course.slug, self.get_object().id])

    def get_form_kwargs(self):
        kwargs = super(UpdateGgvUserAccountView, self).get_form_kwargs()
        kwargs['course_obj'] = self.course
        return kwargs

    def get_initial(self):
        initial = self.initial.copy()
        initial = {'course': self.course, 'perms': self.permissions, 'program_id': self.ggvuser.program_id, 'receive_email_messages': self.ggvuser.receive_email_messages, 'clean_logout': self.ggvuser.clean_logout, 'is_active': self.get_object().is_active}
        
        if 'instructor' in self.permissions:
            initial['receive_notify_email'] = self.ggvuser.receive_notify_email
        
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
        is_active = form.cleaned_data['is_active']

        self.ggvuser.program_id = prog_id
        self.ggvuser.language_pref = language
        self.ggvuser.save()

        #get_user_perms
        curr_permissions = get_perms(self.object, self.course)
        if not curr_permissions:
            curr_permissions = get_user_perms(self.object, self.course)

        # Username changed?
        if not self.object.email == username:
            self.object.email = username
            self.object.save()
            try:
                social_auth_obj = self.object.social_auth.all()[0]
                social_auth_obj.uid = self.object.email
                social_auth_obj.save()
            except:
                pass

        if not self.object.is_active == is_active:
            self.object.is_active = is_active
            self.object.save()

        # Change the user's course?.
        if not self.course.id == course.id:

            for i in curr_permissions:
                assign_perm(i, self.object, course)
                remove_perm(i, self.object, self.course)

            # Change course_context for user's bookmarks
            bks = self.object.bookmarker.all().filter(course_context=self.course)
            for i in bks:
                try:
                    i.course_context = course
                    i.save()
                except IntegrityError as e:
                    i.delete()

            self.course = course



        # Change the user's permissions?
        if perms not in curr_permissions:
            for i in curr_permissions:
                remove_perm(i, self.object, self.course)

            assign_perm(perms, self.object, self.course)

        return super(UpdateGgvUserAccountView, self).form_valid(form)


class UpdateGgvUserView(LoginRequiredMixin, GGVUserViewRestrictedAccessMixin, CourseContextMixin, UpdateView):
    """
    Edits a user's preferences.

    Visibility: all
    """
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
            urlstr = self.request.META['HTTP_REFERER']
            urlstr = urlstr[urlstr.find('q=')+2:]
            return reverse('manage_course', args=[urlstr])
        except:
            return reverse('ggvhome')


class GgvUsersDeactivationView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, View):
    
    def post(self, request, *args, **kwargs):
        try:   
            deactivate_list = request.POST.getlist('deactivate_list')
            request.POST.getlist('activate_list')  
            urlstr = request.POST['url']
            for i in deactivate_list:
                u = User.objects.get(pk=i)
                u.is_active = False
                u.ggvuser.last_deactivation_date = utils.timezone.now()
                u.ggvuser.save()
                u.save()
        except Exception as e:
            pass  # silently fail

        return redirect(urlstr)


class GgvUsersActivationView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, View):
    
    def post(self, request, *args, **kwargs):
        
        try:   
            activate_list = request.POST.getlist('activate_list')  
            urlstr = request.POST['url']
            orgid = request.POST['org']
            ggv_organization = GGVOrganization.objects.get(pk=orgid)
            licenses_in_use = ggv_organization.licenses_in_use()
            license_quota = ggv_organization.user_quota
            license_count = licenses_in_use['count']
            for i in activate_list:
                if license_count < license_quota:
                    u = User.objects.get(pk=i)
                    u.is_active = True
                    u.ggvuser.last_deactivation_date = None
                    u.ggvuser.save()
                    u.save()
                    license_count += 1
                else:
                    messages.warning(request, 'License quota has been exceeded. Some or all requested accounts may not have been activated.')
                    break

        except Exception as e:
            pass  # silently fail

        return redirect(urlstr)


class GgvUserDeleteUnusedAccount(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        try:      
            urlstr = request.POST['url']
            unaccessed_list = request.POST.getlist('unaccessed_list')
            for i in unaccessed_list:
                u = User.objects.get(pk=i)
                if not u.last_login or u.last_login.date() == u.date_joined.date():
                    u.delete()
                               
        except Exception as e:
            pass  # silently fail

        return redirect(urlstr)


class GgvUserArchiveThenDeleteView(CsrfExemptMixin, LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        try:      
            urlstr = request.GET['q']
            user_id = request.POST.getlist('user_id')
            u = User.objects.get(pk=user_id)
            # serialize_user_data(u.id, settings.ARCHIVE_DATA_DIR)
            # u.delete()

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


class AttendanceUpdateAllView(LoginRequiredMixin, TemplateView):
    template_name = "attendance_update_all.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            update_attendance_for_all_users()
        return super(AttendanceUpdateAllView, self).dispatch(request, *args, **kwargs)

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
            prev_type = updated_bk.mark_type
            updated_bk.mark_type = bookmarkform.cleaned_data['mark_type']
            updated_bk.save()

            label = updated_bk.get_mark_type_display()
            if 'span' in request.POST['lesson_lang']:
                label = label.split(',')[1]
            else:
                label = label.split(',')[0]

            data['mark_type'] = label
            data['bookmark_id'] = updated_bk.id
            data['prev_type'] = prev_type

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
        prev_type = self.get_object().mark_type
        self.get_object().delete()
        data = {}
        data['prev_type'] = prev_type
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



