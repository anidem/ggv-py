from collections import OrderedDict
from pytz import timezone
from datetime import datetime
import time
import csv

from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import html, text

from openpyxl import Workbook
from openpyxl.cell import get_column_letter
from openpyxl.styles import Font
from braces.views import LoginRequiredMixin
# from guardian.shortcuts import has_perm

from core.models import Notification, SiteMessage
from core.mixins import AccessRequiredMixin, PrivelegedAccessMixin, RestrictedAccessZoneMixin, CourseContextMixin
from core.utils import UnicodeWriter, GGVExcelWriter, get_daily_log_times
from questions.models import QuestionSet, UserWorksheetStatus
from slidestacks.models import SlideStack
from .models import Course
from .forms import CourseUpdateForm

tz = timezone(settings.TIME_ZONE)


class CourseUpdateView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, UpdateView):
    model = Course
    template_name = 'course_settings.html'
    slug_url_kwarg = 'crs_slug'
    form_class = CourseUpdateForm
    access_object = None


class CourseView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, PrivelegedAccessMixin, DetailView):
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

            context['notifications'] = Notification.objects.filter(user_to_notify=self.request.user)

        else:
            context['instructors'] = course.instructor_list()

        context['deactivated'] = course.deactivated_list()
        context['unvalidated'] = course.unvalidated_list()

        # this provides access to the users full list of courses.
        context['courses'] = [
            Course.objects.get(slug=i) for i in self.request.session['user_courses']]

        try:
            context['site_message'] = SiteMessage.objects.get(url_context=reverse('course', kwargs={'crs_slug': course.slug}))
        except:
            context['site_message'] = None

        return context


class CourseManageView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    """
        Displays an overview of student status and activity. Student status is
        either active, deactivated, or not validated (student account is created
        but student has never logged in.)
        The most recent activity for each active student is displayed.
        This view also provides a Course Settings button to allow instructors to modify
        settings that apply to the course.

        Visibility: sysadmin, staff, and instructor
    """
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

        context['is_manager'] = self.request.user.has_perm('manage', course)
        context['instructors'] = course.instructor_list()
        context['students'] = students
        context['deactivated'] = course.deactivated_list()
        context['unvalidated'] = course.unvalidated_list()
        return context


class UserManageView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    """
        Displays a detailed or raw dump of user activity from activity log table. Data is displayed
        sequentially ordered with most recent activity listed first.

        If request contains query parameter export=csv|xlsx, then response will be a download of csv
        file containing user activity.

        Visibility: sysadmin, staff, instructor
    """

    model = Course
    template_name = 'course_manage_user.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def render_to_response(self, context, **response_kwargs):
        if 'csv' in self.request.GET.get('export', ''):
            response = HttpResponse(content_type='text/csv')
            daystr = datetime.now().strftime('%Y-%m-%d-%I_%M_%p ')
            userstr = context['student_user'].last_name + '-' + context['student_user'].first_name
            filename = userstr + '-' + daystr + '-activity-report.csv'
            response['Content-Disposition'] = 'attachment; filename=' + filename

            writer = UnicodeWriter(response)
            writer.writerow([('%s' % context['student_user'].id), context['student_user'].first_name + ' ' + context['student_user'].last_name, context['student_user'].email, ' Report date: ' + daystr])
            writer.writerow([' '])
            writer.writerow(['Date', 'Total Time on Curriculum', 'Date & Time', 'Activity', 'More Details', 'Subject', 'Current Score'])
            for i in reversed(context['activity_log']):
                writer.writerow([i['day'], i['duration']])
                for j in reversed(i['events']):
                    writer.writerow(['', '', j.timestamp.astimezone(tz).strftime('%b-%d-%Y %I:%M %p'), j.action, html.strip_tags(j.message), j.message_detail or ' ', ''])
            return response

        elif 'xlsx' in self.request.GET.get('export', ''):

            USER_INFO_CELLS = ['A1', 'B1', 'C1', 'D1']

            DATA_COLS = [
                ('A1', u'Date', 15),
                ('B1', u'Total Time on Curriculum', 40),
                ('C1', u'Date & Time', 40),
                ('D1', u'Activity', 50),
                ('E1', u'More Details', 40),
                ('F1', u'Subject', 30),
                ('G1', u'Current Score', 15),
            ]

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            daystr = datetime.now().strftime('%Y-%m-%d-%I_%M_%p ')
            userstr = context['student_user'].last_name + '-' + context['student_user'].first_name
            filename = userstr + '-' + daystr + '-activity-report.xlsx'
            response['Content-Disposition'] = 'attachment; filename=' + filename

            # Openpyxl writer
            writer = Workbook()
            ws = writer.get_active_sheet()
            ws.title = userstr

            # Write user information row and format
            ws.append([context['student_user'].ggvuser.program_id or '', context['student_user'].first_name + ' ' + context['student_user'].last_name, context['student_user'].email, ' Report date: ' + daystr])
            ws.append([])  # Blank row
            for i in USER_INFO_CELLS:
                ws[i].font = Font(size=18, name='Arial', bold=True)

            # Write data column header and format
            for col_num in xrange(len(DATA_COLS)):
                offset = col_num+1
                cell = ws.cell(row=3, column=offset)
                cell.value = DATA_COLS[col_num][1]
                cell.font = Font(size=14, name='Arial')
                # set column width
                ws.column_dimensions[get_column_letter(col_num+1)].width = DATA_COLS[col_num][2]

            # Write data rows
            for i in context['activity_log']:
                ws.append([i['day'], i['duration']])
                for j in i['events']:
                    ws.append(['', '', j['event_time'], j['activity'].action, html.strip_tags(j['activity'].message), j['activity'].message_detail or ' ', j['score'] or ' '])

            writer.save(response)
            return response

        else:
            return super(UserManageView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserManageView, self).get_context_data(**kwargs)
        course = self.get_object()
        user = User.objects.get(pk=self.kwargs['user'])
        
        context['student_user'] = user
        context['activity_log'] = get_daily_log_times(user, course)

        return context


class UserProgressView(LoginRequiredMixin, CourseContextMixin, AccessRequiredMixin, RestrictedAccessZoneMixin, PrivelegedAccessMixin, DetailView):
    """
        Displays progress data for a user/student. This data is filtered here to display
        sequential activity related to a users access and completion of worksheets as well
        as when they view presentations.

        Visibility: sysadmin, staff, instructor
    """
    model = Course
    template_name = 'course_user_progress.html'
    slug_url_kwarg = 'crs_slug'
    access_object = None

    def get(self, request, *args, **kwargs):

        return super(UserProgressView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserProgressView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['user'])
        course = self.get_object()
        context['student_user'] = user
        context['activity_log'] = get_daily_log_times(user, course, ['login', 'logout', 'access-worksheet']) # 'login', 'logout', 'access-worksheet'
        
        return context


class CourseMessageAddView(LoginRequiredMixin, CourseContextMixin, RestrictedAccessZoneMixin, CreateView):
    model = SiteMessage
    template_name = 'ggv_create_page_msg.html'
    course = None
    fields = ['message', 'url_context', 'show']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
        except:
            self.course = None

        return super(CourseMessageAddView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('course', kwargs={'crs_slug': self.course.slug})

    def get_initial(self):
        self.initial = {'url_context':  reverse('course', kwargs={'crs_slug': self.course.slug})}
        return self.initial


class CourseMessageUpdateView(LoginRequiredMixin, CourseContextMixin, RestrictedAccessZoneMixin, UpdateView):
    model = SiteMessage
    template_name = 'ggv_update_page_msg.html'
    course = None
    fields = ['message', 'show']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
        except:
            self.course = None

        return super(CourseMessageUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('course', kwargs={'crs_slug': self.course.slug})


class CourseMessageDeleteView(LoginRequiredMixin, CourseContextMixin, RestrictedAccessZoneMixin, DeleteView):
    model = SiteMessage
    template_name = 'ggv_delete_page_msg.html'
    course = None
    fields = ['message', 'show']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.course = Course.objects.get(slug=kwargs['crs_slug'])
        except:
            self.course = None

        return super(CourseMessageDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('course', kwargs={'crs_slug': self.course.slug})








