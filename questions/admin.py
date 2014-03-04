from django.contrib import admin

from .models import *

admin.site.register(QuestionResponse)
admin.site.register(QuestionOption)
admin.site.register(SimpleQuestion)
admin.site.register(MultipleChoiceQuestion)
