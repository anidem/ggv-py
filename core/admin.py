# core/admin.py

from django.db import models
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from guardian.admin import GuardedModelAdmin

from courses.models import Course
from lessons.models import Lesson, Section
from questions.models import QuestionSet, QuestionResponse, QuestionOption, MultipleChoiceQuestion, ShortAnswerQuestion
from slidestacks.models import SlideStack

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
    model = QuestionOption
    formfield_overrides = {
        models.IntegerField: {'widget': forms.NumberInput},
    }


class QuestionSetInlineAdmin(EditLinkToInlineObject, admin.TabularInline):
    model = MultipleChoiceQuestion
    list_display = ('text', 'select_type', 'question_set', 'display_order')
    extra = 1
    readonly_fields = ('edit_link', )

class QuestionSetInlineShortAnswerAdmin(EditLinkToInlineObject, admin.TabularInline):
    model = ShortAnswerQuestion
    list_display = ('text', 'question_set', 'display_order', 'correct_answer')
    extra = 1
    readonly_fields = ('edit_link', )


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [
        QuestionOptionInlineAdmin,
    ]
    list_display = ('text', 'select_type', 'question_set', 'display_order')
    list_editable = ('display_order',)
    list_filter = ('question_set',)

    formfield_overrides = {
        models.IntegerField: {'widget': forms.NumberInput},
    }

class ShortAnswerQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_set', 'display_order')
    list_editable = ('display_order',)
    list_filter = ('question_set',)


class WorksheetInlineAdmin(admin.TabularInline):
    model = QuestionSet

class SlideStackInlineAdmin(admin.TabularInline):
    model = SlideStack

class SlideStackAdmin(admin.ModelAdmin):
    model = SlideStack
    list_display = ('lesson', 'title', 'section',  'asset', 'display_order')
    # list_editable = ('section',)
    list_filter = ('lesson', 'section',)


class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'title', 'section', 'display_order')
    # list_editable = ('section',)
    list_filter = ('lesson', 'section',)

    inlines = [
        QuestionSetInlineAdmin, QuestionSetInlineShortAnswerAdmin,
    ]

class CourseAdmin(GuardedModelAdmin):
    model = Course
    list_display = ('title', 'short_name', 'access_code', 'lesson_list')


class LessonAdmin(GuardedModelAdmin):
    inlines = [
        WorksheetInlineAdmin, SlideStackInlineAdmin,
    ]

class SectionAdmin(GuardedModelAdmin):
    list_display = ('lesson', 'title', 'display_order')

admin.site.register(Course, CourseAdmin, Media=ExtraMedia)
admin.site.register(Lesson, LessonAdmin, Media=ExtraMedia)
admin.site.register(Section, SectionAdmin, Media=ExtraMedia)
admin.site.register(SlideStack, SlideStackAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin, Media=ExtraMedia)
admin.site.register(QuestionResponse)
admin.site.register(ShortAnswerQuestion, ShortAnswerQuestionAdmin, Media=ExtraMedia)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin, Media=ExtraMedia)
