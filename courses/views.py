from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from operator import attrgetter

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from guardian.shortcuts import get_users_with_perms, get_objects_for_user, get_perms

from core.mixins import AccessRequiredMixin

from .models import Course


class CourseView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = Course
    template_name = 'course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        lessons = course.lesson_list()
        context['eng_lessons'] = lessons.filter(language='eng').order_by('subject')
        context['span_lessons'] = lessons.filter(language='span').order_by('subject')
        context['courses'] = get_objects_for_user(
            self.request.user, 'view_course', Course)

        instructors = []
        students = []
        for i in course.member_list():
            if i.has_perm('courses.edit_course', course):
                instructors.append(i)
            else:
                students.append(i)
        context['instructors'] = sorted(instructors)
        context['students'] = sorted(students)
        return context