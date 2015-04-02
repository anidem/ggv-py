# core/admin.py
from django.db import models
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from guardian.admin import GuardedModelAdmin

from courses.models import Course, CourseLesson
from lessons.models import Lesson, Section
from questions.models import QuestionSet, QuestionResponse, OptionQuestion, TextQuestion, Option
from slidestacks.models import SlideStack
from notes.models import UserNote
from core.models import ActivityLog, GGVUser, Bookmark


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
    list_display = ('display_text', 'display_order', 'display_image', 'display_pdf')
    list_filter = ('question_set', 'question_set__lesson')
    list_editable = ('display_order', 'display_image',)
    inlines = [QuestionOptionInlineAdmin]


class TextQuestionAdmin(admin.ModelAdmin):
    list_display = ('display_text', 'correct', 'display_order', 'display_image', 'display_pdf')
    list_filter = ('question_set', 'question_set__lesson')
    list_editable = ('display_order', 'display_image',)

class CourseAdmin(GuardedModelAdmin):
    model = Course
    list_display = ('title', 'slug', 'access_code', 'lesson_list')
    inlines = [
        LessonInlineAdmin,
    ]

class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'lesson')
    list_filter = ('course',)



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
    list_filter = ('timestamp', 'user', 'action' )

admin.site.register(Course, CourseAdmin, Media=ExtraMedia)
admin.site.register(CourseLesson, CourseLessonAdmin)
admin.site.register(Lesson, LessonAdmin, Media=ExtraMedia)
admin.site.register(Section, SectionAdmin, Media=ExtraMedia)
admin.site.register(SlideStack, SlideStackAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin, Media=ExtraMedia)
admin.site.register(OptionQuestion, OptionQuestionAdmin, Media=ExtraMedia)
admin.site.register(TextQuestion, TextQuestionAdmin, Media=ExtraMedia)
admin.site.register(QuestionResponse)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(GGVUser)
admin.site.register(Bookmark)
# admin.site.register(ShortAnswerQuestion, ShortAnswerQuestionAdmin, Media=ExtraMedia)
# admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin, Media=ExtraMedia)
admin.site.register(UserNote)


