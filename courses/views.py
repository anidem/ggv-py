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
    slug_url_kwarg = 'crs_slug'
    access_object = 'course'

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        course = self.get_object()
        lessons = course.lesson_list()
        context['eng_lessons'] = lessons.filter(lesson__language='eng').order_by('lesson__subject')
        context['span_lessons'] = lessons.filter(lesson__language='span').order_by('lesson__subject')
        
        instructors = []
        students = []
        for i, j in course.member_list().items():
            if 'access' in j:
                students.append(i)
            elif 'instructor' in j:
                instructors.append(i)

        # this provides access to the users full list of courses.
        context['courses'] = [Course.objects.get(slug=i) for i in self.request.session['user_courses']]
        context['instructors'] = instructors
        context['students'] = students

        return context