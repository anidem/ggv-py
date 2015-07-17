# core/views.py
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail


from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin
from guardian.shortcuts import assign_perm

from courses.models import Course

from .models import Bookmark, GGVUser, SiteMessage, Notification
from .forms import BookmarkForm, GgvUserCreateForm, GgvUserSettingsForm, GgvUserStudentSettingsForm
from .mixins import CourseContextMixin
from .signals import *


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['site_message'] = SiteMessage.objects.get(url_context='http://www.ggvinteractive.com/')
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
    success_url = reverse_lazy('view_user')
    form_class = GgvUserCreateForm
    course = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
        except:
            self.course = None

        return super(CreateGgvUserView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('create_user', args=[self.kwargs['crs_slug']])

    def get_initial(self):
        # initial = self.initial.copy()
        self.initial = {
            'course': self.course, 'language': 'english', 'is_active': False, 'perms': 'access'}
        return self.initial

    def form_valid(self, form):
        self.object = form.save()
        language = form.cleaned_data['language']
        course = form.cleaned_data['course']
        perms = form.cleaned_data['perms']
        ggvuser = GGVUser(user=self.object, language_pref=language)
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


class UpdateGgvUserView(LoginRequiredMixin, CourseContextMixin, UpdateView):
    model = GGVUser
    template_name = "user_edit.html"
    form_class = GgvUserStudentSettingsForm
    success_url = reverse_lazy('ggvhome')

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('instructor') or request.user.has_perm('manage'):
            self.form_class = GgvUserSettingsForm

        return super(UpdateGgvUserView, self).dispatch(request, *args, **kwargs)


class ListGgvUserView(LoginRequiredMixin, CourseContextMixin, ListView):
    model = User
    template_name = 'user_view.html'


class GgvUserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_view.html'


class ActivateView(LoginRequiredMixin, TemplateView):
    template_name = 'activate.html'


class AccessForbiddenView(TemplateView):
    template_name = 'access_forbidden.html'


class ActivityLogView(TemplateView):
    pass


class SendEmailMessage(LoginRequiredMixin, TemplateView)
    pass


class CreateMessageView(TemplateView):
    pass

# messages.debug(request, '%s SQL statements were executed.' % count)
# messages.info(request, 'Three credits remain in your account.')
# messages.success(request, 'Profile details updated.')
# messages.warning(request, 'Your account expires in three days.')
# messages.error(request, 'Document deleted.')


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
