# forms.py

from django import forms
from django.forms import ModelForm

from django.contrib.contenttypes.models import ContentType

from .models import PretestAccount, PretestUser, PretestQuestionResponse, PretestUserCompletion

class LoginTokenForm(forms.Form):
    email = forms.EmailField()
    token = forms.CharField()

    def clean(self):
        data = super(LoginTokenForm, self).clean()
        try:
            pretester = PretestUser.objects.filter(email=data['email']).get(access_token=data['token'])
        except:
            raise forms.ValidationError('email and/or token were invalid.', code='invalid_creds')


class TokenGeneratorForm(forms.Form):
    account = forms.ModelChoiceField(queryset=PretestAccount.objects.all())
    num_tokens = forms.IntegerField(min_value=1)
    
    class Meta:
        fields = ['account', 'num_tokens']


class LanguageChoiceForm(ModelForm):

    def clean(self):
        data = super(LanguageChoiceForm, self).clean()
        if data['language_pref'] == None:
            raise forms.ValidationError('A language preference must be indicated.')

    class Meta:
        model = PretestUser
        fields = ['language_pref']


class PretestUserUpdateForm(ModelForm):
    account_selector = forms.ChoiceField(choices=[], required=False)
        
    def __init__(self, *args, **kwargs):
        super(PretestUserUpdateForm, self).__init__(*args, **kwargs)
        if self.initial['users']:
            self.fields['account_selector'].choices = [(' ',' ')] + [(i.id, str(i.first_name + ' ' + i.last_name)) for i in self.initial['users']]
            self.fields['account_selector'].label = 'Choose pretest user from list (optional):'
        else:
            del self.fields['account_selector']

    class Meta:
        model = PretestUser
        fields = ['account_selector', 'email', 'first_name', 'last_name', 'program_id']
        labels = {'email': 'Enter a valid email address for pretest user.'}


class PretestCompleteConfirmForm(ModelForm):

    class Meta:
        model = PretestUserCompletion
        fields = ['confirm_completed']
        widgets = {'confirm_completed': forms.HiddenInput(),}


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