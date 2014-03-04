from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from guardian.shortcuts import get_users_with_perms

from lessons.models import Lesson


class Course(models.Model):
	title = models.CharField(max_length=256)
	short_name = models.CharField(max_length=32)
	lessons = models.ManyToManyField(Lesson, related_name='associated_courses')
	access_code = models.CharField(max_length=8, null=True, blank=True)
	
	class Meta:
		permissions = (
			("view_course", "Access course"),
		)
	
	def member_list(self):
		return get_users_with_perms(self)

	def lesson_list(self):
		return self.lessons.all()

	def check_membership(self, user):
		return user.has_perm('core.view_course', self)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('course', args=[str(self.id)])
