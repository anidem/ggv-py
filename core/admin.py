# core/admin.py

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Course
from lessons.models import Lesson, Activity


class ActivityInline(admin.TabularInline):
	model = Activity
	fk_name = 'lesson'
	

class CourseAdmin(GuardedModelAdmin):
	pass


class LessonAdmin(GuardedModelAdmin):
	inlines = [
		ActivityInline,
	]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
