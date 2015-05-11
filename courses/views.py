from operator import attrgetter
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin

from core.mixins import AccessRequiredMixin, PrivelegedAccessMixin, RestrictedAccessZoneMixin
from questions.models import QuestionSet
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
        activity = []
        for i in user.activitylog.all().extra({'day': 'date(timestamp)'}):
            if i.action == 'completed-worksheet':
                try:
                    wurl = i.message.split('/')
                    course = Course.objects.get(slug=wurl[2])
                    worksheet = QuestionSet.objects.get(pk=wurl[4])
                    report_url = reverse('worksheet_user_report', args=[course.slug, worksheet.id, user.id])
                    report = worksheet.get_user_responses(user, worksheet.get_ordered_question_list(), course)
                    score = report['grade']

                    activity.append({'activity': i, 'report_url': report_url, 'worksheet': worksheet, 'score': score})
                except:
                    pass  # malformed log message. proceed silently...
            elif i.action == 'access-presentation' or i.action == 'access-worksheet':
                activity.append({'activity': i, 'report_url': i.message, 'worksheet': None, 'score': None})

            else:
                activity.append({'activity': i, 'report_url': i.message, 'worksheet': None, 'score': None})

        context['student_user'] = user
        context['activity_log'] = activity

        return context
