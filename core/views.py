from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, CsrfExemptMixin
from guardian.shortcuts import get_users_with_perms, get_objects_for_user

from .models import Course
from .mixins import AccessRequiredMixin, AccessCodeRequiredMixin


@receiver(user_logged_in)
def init_session(sender, **kwargs):
	request = kwargs['request']
	user = kwargs['user']
	# courses = user.course_membership.values_list('id', flat=True)
	courses = get_objects_for_user(user, 'view_course', Course).values_list('id', flat=True)
	request.session['user_courses'] = []
	for i in courses:
		request.session['user_courses'].append(i)

	print request.session['user_courses']

class IndexView(TemplateView):
	template_name = 'index.html'	

class HomeView(LoginRequiredMixin, TemplateView):
	template_name = 'ggv.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['courses'] = get_objects_for_user(self.request.user, 'view_course', Course)
		return context


class CourseView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
	model = Course
	template_name = 'course.html'

	def get_context_data(self, **kwargs):
		context = super(CourseView, self).get_context_data(**kwargs)
		course = self.get_object()
		context['lessons'] = course.lesson_list()
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
