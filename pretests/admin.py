from django.contrib import admin

from .models import PretestUser, PretestQuestionResponse, PretestAccount, PretestUserCompletion


class PretestAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'contact_email', 'contact_phone', 'ggv_org',)
    list_filter = ('ggv_org',)


class PretestUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_token', 'email', 'account', 'first_name', 'last_name', 'program_id', 'language_pref')
    list_filter = ('account',)


class PretestQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('pretestuser', 'pretestuser_name', 'response', 'iscorrect', 'grade_request_sent') 
    list_filter = ('pretestuser__account', 'pretestuser__last_name', 'pretestuser__email',)

    def pretestuser_name(self, obj):
        return ("%s %s" % (obj.pretestuser.first_name, obj.pretestuser.last_name))


class PretestUserCompletionAdmin(admin.ModelAdmin):
    list_display = ('created', 'pretestuser_name', 'pretestuser', 'completed_pretest', 'confirm_completed', 'notification_sent')
    list_filter = ('pretestuser__account', ('completed_pretest', admin.RelatedOnlyFieldListFilter), 'pretestuser__last_name',)
    
    def pretestuser_name(self, obj):
        return ("%s %s" % (obj.pretestuser.first_name, obj.pretestuser.last_name))


admin.site.register(PretestAccount, PretestAccountAdmin)
admin.site.register(PretestUser, PretestUserAdmin)
admin.site.register(PretestQuestionResponse, PretestQuestionResponseAdmin)
admin.site.register(PretestUserCompletion, PretestUserCompletionAdmin)
