from django.contrib import admin

from .models import PretestUser, PretestQuestionResponse, PretestAccount

admin.site.register(PretestAccount)
admin.site.register(PretestUser)
admin.site.register(PretestQuestionResponse)
