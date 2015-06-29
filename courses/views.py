from operator import attrgetter
from collections import OrderedDict, namedtuple
from datetime import datetime
from pytz import timezone

from django.views.generic import DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# from django.utils import timezone
from django.conf import settings


from braces.views import LoginRequiredMixin

from core.mixins import AccessRequiredMixin, PrivelegedAccessMixin, RestrictedAccessZoneMixin
from questions.models import QuestionSet
from slidestacks.models import SlideStack
from .models import Course
from .forms import CourseUpdateForm

tz = timezone(settings.TIME_ZONE)


class CourseUpdateView(LoginRequiredMixin, AccessRequiredMixin, UpdateView):
    model = Course
    template_name = 'course_edit.html'
    slug_url_kwarg = 'crs_slug'
    form_class = CourseUpdateForm
    access_object = None


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

        if self.request.user.is_staff or context['is_instructor'] or context['is_manager']:
            students = course.student_list()


            instructors = course.instructor_list()

            context['instructors'] = instructors
            context['students'] = students
        else:
            context['instructors'] = course.instructor_list()

        context['deactivated'] = course.deactivated_list()
        context['unvalidated'] = course.unvalidated_list()

        # this provides access to the users full list of courses.
        context['courses'] = [
            Course.objects.get(slug=i) for i in self.request.session['user_courses']]

        # context['instructors'] = course.instructor_list()
        # context['students'] = course.student_list(extra_details=True)
        return context


class CourseManageView(LoginRequiredMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    model = Course
    template_name = 'course_manage.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def get_context_data(self, **kwargs):
        context = super(CourseManageView, self).get_context_data(**kwargs)
        course = self.get_object()
        students = []
        for i in course.student_list():
            try:
                activity = i.activitylog.all()[0]
                students.append((i, {'recent_act': activity.action, 'recent_time': activity.timestamp}))
            except:
                pass  # student[i] has no activity on record. Move on, nothing to see here.

        context['instructors'] = course.instructor_list()
        context['students'] = students
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

        """
        (activitylog entry, score)
        """
        activity = OrderedDict()  # {'day': {'duration': n, 'activity_list':[dicts]}
        for i in user.activitylog.all():
            tkey = i.timestamp.astimezone(tz).strftime('%b-%d-%Y')

            try:
                activity[tkey]
            except:
                activity[tkey] = []

            if i.action == 'completed-worksheet':
                try:
                    wurl = i.message.split('/')
                    course = Course.objects.get(slug=wurl[2])
                    worksheet = QuestionSet.objects.get(pk=wurl[4])
                    report_url = reverse('worksheet_user_report', args=[course.slug, worksheet.id, user.id])

                    activity[tkey].append({'activity': i, 'report_url': report_url, 'worksheet': worksheet})
                except:
                    pass  # malformed log message. proceed silently...

            elif i.action == 'access-presentation' or i.action == 'access-worksheet':
                activity[tkey].append({'activity': i, 'report_url': i.message, 'worksheet': None, 'score': None})

            else:
                activity[tkey].append({'activity': i, 'report_url': i.message, 'worksheet': None, 'score': None})

        context['student_user'] = user
        context['activity_log'] = activity

        return context


class UserProgressView(LoginRequiredMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    model = Course
    template_name = 'course_user_progress.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def get(self, request, *args, **kwargs):
        # course = Course.objects.get(slug=self.kwargs['crs_slug'])
        return super(UserProgressView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserProgressView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['user'])

        """
        (activitylog entry, score)
        """
        activity = OrderedDict()
        for i in user.activitylog.all():


            activity_info = []
            try:
                activity_info = [j for j in i.message.split('/ggv/')[1].split('/')]

            except:
                pass

            activity_dict = None
            if i.action == 'completed-worksheet':
                try:
                    crs, ws_id = activity_info[0], activity_info[2]
                    course = Course.objects.get(slug=crs)

                    worksheet = QuestionSet.objects.get(pk=ws_id)
                    report_url = reverse('worksheet_user_report', args=[course.slug, worksheet.id, user.id])
                    report = worksheet.get_user_responses(user, worksheet.get_ordered_question_list(), course)
                    score = report['grade']

                    activity_dict = {'activity': i, 'access_time': None, 'completed_time': i.timestamp, 'report_url': report_url, 'course': course,  'content': worksheet, 'score': score}
                except:
                    pass  # malformed log message. proceed silently...

            elif i.action == 'access-presentation':
                try:
                    crs, stack_id = activity_info[0], activity_info[2]
                    stack = SlideStack.objects.get(pk=stack_id)
                    course = Course.objects.get(slug=crs)
                    activity_dict = {'activity': i, 'access_time': i.timestamp, 'completed_time': None, 'report_url': i.message, 'course': self.get_object(), 'content': stack, 'score': None}
                except:
                    pass

            if activity_dict:

                tkey = i.timestamp.astimezone(tz).strftime('%b-%d-%Y')
                try:
                    activity[tkey].append(activity_dict)
                except:
                    activity[tkey] = []
                    activity[tkey].append(activity_dict)

        context['student_user'] = user
        context['activity_log'] = activity

        return context



