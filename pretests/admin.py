from django.contrib import admin

from .models import PretestUser, PretestQuestionResponse, PretestAccount, PretestUserCompletion


class PretestAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'contact_email', 'contact_phone', 'ggv_org',)
    list_filter = ('ggv_org',)


class PretestUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_token', 'email', 'account', 'first_name', 'last_name', 'program_id', 'language_pref')
    list_filter = ('account',)


class PretestQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('pretestuser', 'response', 'iscorrect',)
    list_filter = ('pretestuser',)


class PretestUserCompletionAdmin(admin.ModelAdmin):
    list_display = ('created', 'pretestuser', 'completed_pretest',)
    list_filter = ('completed_pretest', 'pretestuser',)

admin.site.register(PretestAccount, PretestAccountAdmin)
admin.site.register(PretestUser, PretestUserAdmin)
admin.site.register(PretestQuestionResponse, PretestQuestionResponseAdmin)
admin.site.register(PretestUserCompletion, PretestUserCompletionAdmin)
