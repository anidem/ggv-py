from operator import attrgetter
from django.views.generic import DetailView
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin

from core.mixins import AccessRequiredMixin, PrivelegedAccessMixin, RestrictedAccessZoneMixin
from core.models import ActivityLog
from .models import Course


class CourseView(LoginRequiredMixin, AccessRequiredMixin, PrivelegedAccessMixin, DetailView):
    model = Course
    template_name = 'course.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        lessons = course.lesson_list()
        context['eng_lessons'] = lessons.filter(
            lesson__language='eng').order_by('lesson__subject')
        context['span_lessons'] = lessons.filter(
            lesson__language='span').order_by('lesson__subject')

        # this provides access to the users full list of courses.
        context['courses'] = [
            Course.objects.get(slug=i) for i in self.request.session['user_courses']]
        context['instructors'] = course.instructor_list()
        context['students'] = course.student_list(extra_details=True)
        return context


class CourseManageView(LoginRequiredMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    model = Course
    template_name = 'course_manage.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def get_context_data(self, **kwargs):
        context = super(CourseManageView, self).get_context_data(**kwargs)
        course = self.get_object()
        context['instructors'] = course.instructor_list()
        context['students'] = sorted(
            course.student_list(), key=attrgetter('last_login'), reverse=True)
        context['deactivated'] = course.deactivated_list()
        context['unvalidated'] = course.unvalidated_list()
        return context


class UserManageView(LoginRequiredMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    model = Course
    template_name = 'course_manage_user.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def get_context_data(self, **kwargs):
        context = super(UserManageView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['user'])

        context['student_user'] = user
        context['activity_log'] = ActivityLog.objects.filter(
            user=user).extra({'day': 'date(timestamp)'})

        return context
