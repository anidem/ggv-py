# core/admin.py
from django.db import models
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from guardian.admin import GuardedModelAdmin

from courses.models import GGVOrganization, Course, CourseLesson, CourseTag, TaggedCourse, CourseGrader
from lessons.models import Lesson, Section
from questions.models import QuestionSet, QuestionResponse, OptionQuestion, TextQuestion, Option, UserWorksheetStatus, ExtraInfo
from slidestacks.models import SlideStack
from supportmedia.models import ExternalMedia
from notes.models import UserNote
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from core.models import ActivityLog, GGVUser, Bookmark, SiteMessage, SitePage, AttendanceTracker

UserAdmin.list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'last_login', 'date_joined')
UserAdmin.list_editable = ('is_active',)


class ExtraMedia:
    js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/js/tinymce_setup.js',
    ]


class EditLinkToInlineObject(object):

    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.module_name),  args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}" target="_blank" onclick="return showAddAnotherPopup(this);">edit</a>'.format(u=url))
        else:
            return ''


class QuestionOptionInlineAdmin(admin.TabularInline):
    model = Option
    formfield_overrides = {
        models.IntegerField: {'widget': forms.NumberInput},
    }


# class QuestionSetInlineAdmin(EditLinkToInlineObject, admin.TabularInline):
#     model = MultipleChoiceQuestion
#     list_display = ('text', 'select_type', 'question_set', 'display_order')
#     extra = 1
#     readonly_fields = ('edit_link', )

# class QuestionSetInlineShortAnswerAdmin(EditLinkToInlineObject, admin.TabularInline):
#     model = ShortAnswerQuestion
#     list_display = ('text', 'question_set', 'display_order', 'correct_answer')
#     extra = 1
#     readonly_fields = ('edit_link', )


# class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
#     inlines = [
#         QuestionOptionInlineAdmin,
#     ]
#     list_display = ('text', 'select_type', 'question_set', 'display_order')
#     list_editable = ('display_order',)
#     list_filter = ('question_set',)

#     formfield_overrides = {
#         models.IntegerField: {'widget': forms.NumberInput},
#     }

# class ShortAnswerQuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'question_set', 'display_order')
#     list_editable = ('display_order',)
#     list_filter = ('question_set',)


class WorksheetInlineAdmin(admin.TabularInline):
    model = QuestionSet


class SlideStackInlineAdmin(admin.TabularInline):
    model = SlideStack


class LessonInlineAdmin(admin.TabularInline):
    model = CourseLesson
    extra = 8


class SlideStackAdmin(admin.ModelAdmin):
    model = SlideStack
    list_display = ('title', 'lesson', 'section',  'asset', 'display_order')
    list_filter = ('lesson', 'section',)
    list_editable = ('asset',)


class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lesson', 'section', 'display_order')
    list_filter = ('lesson', 'section',)
    list_editable = ('title', 'lesson', 'section', 'display_order',)

#     inlines = [
#         QuestionSetInlineAdmin, QuestionSetInlineShortAnswerAdmin,
#     ]


class OptionQuestionAdmin(admin.ModelAdmin):
    list_display = ('display_text', 'display_order',
                    'display_image', 'display_pdf', 'response_required', 'extra_info')
    list_filter = ('question_set', 'question_set__lesson', 'content_area', 'extra_info')
    list_editable = ('display_order', 'display_image', 'response_required')
    inlines = [QuestionOptionInlineAdmin]


class TextQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'correct', 'display_order',
                    'display_image', 'display_pdf', 'response_required','extra_info')
    list_filter = ('question_set', 'question_set__lesson', 'content_area', 'extra_info', 'correct', 'response_required')
    list_editable = ('display_order', 'display_image', 'response_required', 'extra_info')


class CourseAdmin(GuardedModelAdmin):
    model = Course
    list_display = ('title', 'ggv_organization', 'slug')
    list_filter = ('title', 'ggv_organization')
    list_editable = ('ggv_organization',)
    # inlines = [
    #     LessonInlineAdmin,
    # ]


class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'lesson')
    list_filter = ('course',)


class CourseGraderAdmin(admin.ModelAdmin):
    list_display = ('course', 'grader')
    list_filter = ('course__ggv_organization',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == "grader":
        #     kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super(CourseGraderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class LessonAdmin(GuardedModelAdmin):
    list_display = ('title', 'subject', 'icon_class', 'language')
    list_editable = ('subject', 'icon_class', 'language')
    inlines = [
        WorksheetInlineAdmin, SlideStackInlineAdmin,
    ]


class SectionAdmin(GuardedModelAdmin):
    list_display = ('id', 'lesson', 'title', 'display_order')
    list_editable = ('lesson', 'title', 'display_order')
    list_filter = ('lesson', )


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'message')
    list_filter = ('timestamp', 'user', 'action')

class AttendanceTrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'datestamp', 'datestr', 'code')
    list_filter = ('user',)


class GGVUserInline(admin.TabularInline):
    """ Will be inserted in admin panel for user (at bottom)"""
    model = GGVUser


class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_active', 'is_staff', 'last_login', 'date_joined')
    inlines = [GGVUserInline, ]


class GGVUserAdmin(admin.ModelAdmin):
    list_display = ('program_id', 'user', 'language_pref', 'clean_logout', )
    list_editable = ('user', 'language_pref', 'clean_logout', )


class GGVOrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'license_id', 'title', 'user_quota', 'quota_start_date', 'business_contact_email', 'business_contact_phone')

class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'response', 'modified', 'content_type', 'object_id', 'iscorrect')
    list_filter = ('user__email', 'content_type')

admin.site.register(GGVOrganization, GGVOrganizationAdmin)
admin.site.register(Course, CourseAdmin, Media=ExtraMedia)
admin.site.register(CourseLesson, CourseLessonAdmin)
admin.site.register(CourseTag)
admin.site.register(TaggedCourse)
admin.site.register(CourseGrader, CourseGraderAdmin)
admin.site.register(Lesson, LessonAdmin, Media=ExtraMedia)
admin.site.register(Section, SectionAdmin, Media=ExtraMedia)
admin.site.register(SlideStack, SlideStackAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin, Media=ExtraMedia)
admin.site.register(OptionQuestion, OptionQuestionAdmin, Media=ExtraMedia)
admin.site.register(TextQuestion, TextQuestionAdmin, Media=ExtraMedia)
admin.site.register(QuestionResponse, QuestionResponseAdmin)
admin.site.register(ExtraInfo)
admin.site.register(ExternalMedia)
admin.site.register(UserWorksheetStatus)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(AttendanceTracker, AttendanceTrackerAdmin)
admin.site.register(GGVUser, GGVUserAdmin)
admin.site.register(Bookmark)
admin.site.register(SiteMessage)
admin.site.register(SitePage)
admin.site.register(UserNote)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
