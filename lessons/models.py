from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Lesson(models.Model):
	MATH = 'Math'
	SPMATH = 'SP_MATH'
	SCIENCE = 'SCI'
	SPSCIENCE = 'SP_SCI'
	SOCSTUDIES = 'SOCSTUDIES'
	SPSOCSTUDIES = 'SP_SOCSTUDIES'
	WRITING = 'WRITING'
	SPWRITING = 'SP_WRITING'

	LESSON_SUBJECTS = (
		(MATH, 'Math'),
		(SPMATH, 'Math en Espanol'),
		(SCIENCE, 'Science'),
		(SPSCIENCE, 'Science en Espanol'),
		(SOCSTUDIES, 'Social Studies'),
		(SPSOCSTUDIES, 'Social Studies en Espanol'),
		(WRITING, 'Writing'),
		(SPWRITING, 'Writing en Espanol'),
	)

	title = models.CharField(max_length=256, default='Subject')
	subject = models.CharField(max_length=32, choices=LESSON_SUBJECTS)

	def check_membership(self, user):
		courses = self.associated_courses.all()
		for i in courses:
			if user.has_perm('core.view_course', i):
				return True
		return False

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('lesson', args=[str(self.id)])


class Activity(models.Model):
	title = models.CharField(max_length=256)
	assets = models.CharField(max_length=256)
	lesson = models.ForeignKey(Lesson, null=True, blank=True)
	section = models.ForeignKey('Section', null=True, blank=True)

	def check_membership(self, user):
		return self.lesson.check_membership(user)
	
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('activity', args=[str(self.id)])

class Section(models.Model):
	title = models.CharField(max_length=256)

	def __unicode__(self):
		return self.title



