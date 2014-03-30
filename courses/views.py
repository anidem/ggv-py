from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from guardian.shortcuts import get_users_with_perms, get_objects_for_user

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin

from .models import Course


class CourseView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = Course
    template_name = 'course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        context['lessons'] = course.lesson_list()
        context['courses'] = get_objects_for_user(
            self.request.user, 'view_course', Course)
        context['members'] = get_users_with_perms(course)
        return context


class StudentCourseView(AccessCodeRequiredMixin, DetailView):
    model = Course
    template_name = 'course_student.html'

    def get_context_data(self, **kwargs):
        context = super(StudentCourseView, self).get_context_data(**kwargs)
        context['lessons'] = self.get_object().lesson_list()
        self.request.session['student_visitor']
        return context
