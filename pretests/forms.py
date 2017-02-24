# forms.py

from django import forms
from django.forms import ModelForm

from django.contrib.contenttypes.models import ContentType

from .models import PretestUser, PretestQuestionResponse

class LoginTokenForm(forms.Form):
    email = forms.EmailField()
    token = forms.CharField()

    def clean(self):
        data = super(LoginTokenForm, self).clean()
        try:
            pretester = PretestUser.objects.filter(email=data['email']).get(access_token=data['token'])
        except:
            raise forms.ValidationError('email and/or token were invalid.', code='invalid_creds')

    class Meta:
        model = PretestQuestionResponse
        fields = ['pretestuser', 'content_type', 'object_id', 'response']
        widgets = {
            'pretestuser': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput()
        }

class PretestQuestionResponseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PretestQuestionResponseForm, self).__init__(*args, **kwargs)
        try:
            self.fields['response'] = self.initial['question'].get_input_widget()
        except Exception as e:
            return
    
    class Meta:
        model = PretestQuestionResponse
        fields = ['pretestuser', 'content_type', 'object_id', 'response']
        widgets = {
            'pretestuser': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput()
        }