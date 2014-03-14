from django.contrib import admin

from .models import QuestionResponse, QuestionOption, SimpleQuestion, MultipleChoiceQuestion

class QuestionOptionInline(admin.TabularInline):
	model = MultipleChoiceQuestion.options.through

class MultipleChoiceQuestionInline(admin.ModelAdmin):
	inlines = [ 
		QuestionOptionInline,
	]
	exclude = ('options',)
	
admin.site.register(QuestionResponse)
admin.site.register(QuestionOption)
admin.site.register(SimpleQuestion)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionInline)
