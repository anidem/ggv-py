from django.contrib import admin

from .models import Survey, SurveyTextQuestion, SurveyOptionQuestion, SurveyQuestionOption

admin.site.register(Survey)
admin.site.register(SurveyTextQuestion)
admin.site.register(SurveyOptionQuestion)
admin.site.register(SurveyQuestionOption)