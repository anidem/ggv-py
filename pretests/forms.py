# forms.py

from django import forms
from django.forms import ModelForm

from django.forms.widgets import Select, SelectMultiple
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape



from django.contrib.contenttypes.models import ContentType

from .models import PretestAccount, PretestUser, PretestQuestionResponse, PretestUserCompletion, PretestUserAssignment, SPN_PRETESTS_LESSON_ID,ENG_PRETESTS_LESSON_ID
from lessons.models import Lesson


def custom_choices(choices):
    mod_choices = []
    for i in choices:
        if i[0] == 150:
            mod_choices.append((i[0], {'label': i[1], 'disabled': True}))
        else:
            mod_choices.append(i)
    return mod_choices

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


class MultipleSelectWithDisabledCheckbox(forms.CheckboxSelectMultiple):
    """
    Subclass of Django's CheckboxSelectMultiple widget that allows disabling options.
    To disable an option, pass a dict instead of a string for its label,
    of the form: {'label': 'option label', 'disabled': True}

    Adapted from: https://www.djangosnippets.org/snippets/2453/
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        disabled = False
        if isinstance(label, dict):
            label, disabled = label['label'], label['disabled']
        option_dict = super(MultipleSelectWithDisabledCheckbox, self).create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if disabled:
            option_dict['attrs']['disabled'] = 'disabled'
        print option_dict
        return option_dict

    def render_option(self, selected_choices, option_value, option_label):
        print 'overriding option render'
        option_value = force_unicode(option_value)
        if (option_value in selected_choices):
            selected_html = u'checked'
        else:
            selected_html = ''
        disabled_html = ''
        if isinstance(option_label, dict):
            if dict.get(option_label, 'disabled'):
                disabled_html = u'disabled'
            option_label = option_label['label']
        return u'<label><input type="checkbox" value="%s"%s%s>%s</label>' % (
            escape(option_value), selected_html, disabled_html,
            conditional_escape(force_unicode(option_label)))


class PretestSelectionForm(forms.Form):
    eng_pretest_choices = [(i.pk, i.title ) for i in Lesson.objects.get(pk=ENG_PRETESTS_LESSON_ID).activities()]
    spn_pretest_choices = [(i.pk, i.title ) for i in Lesson.objects.get(pk=SPN_PRETESTS_LESSON_ID).activities()]

    eng_select_all = forms.BooleanField(label='Select all four English pretests', required=False)
    eng_pretests = forms.MultipleChoiceField(required=False, label='', widget=forms.CheckboxSelectMultiple, choices=eng_pretest_choices,)
    
    spn_select_all = forms.BooleanField(label='Select all four Spanish pretests', required=False)  
    spn_pretests = forms.MultipleChoiceField(required=False, label='', widget=forms.CheckboxSelectMultiple, choices=spn_pretest_choices,)    
    
    def __init__(self, *args, **kwargs):
        super(PretestSelectionForm, self).__init__(*args, **kwargs)        

    class Meta:
        fields = ['eng_select_all', 'eng_pretests', 'spn_pretests', 'spn_select_all']


class PretestUserCreateForm(ModelForm):
    account_selector = forms.ChoiceField(choices=[], required=False)
    
        
    def __init__(self, *args, **kwargs):
        super(PretestUserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        if self.initial['users']:
            self.fields['account_selector'].choices = [(' ','--')] + [(i.id, unicode(i.first_name + u' ' + i.last_name + u', ' + i.email)) for i in self.initial['users']]
            self.fields['account_selector'].label = 'Choose an examinee from a list of users that are part of your organization. (optional):'
        else:
            # accounts are loaded from google db. remove the selector from this form. google selector form is defined in html and javascript.
            del self.fields['account_selector']

    class Meta:
        model = PretestUser
        fields = ['account_selector', 'account', 'email', 'first_name', 'last_name', 'program_id']
        labels = {
            'email': 'Enter a valid email address for a pretest examinee.', 
            'program_id': 'Program ID (optional)'}
        widgets = {'account': forms.HiddenInput()}


class PretestUserUpdateForm(ModelForm):
    account_selector = forms.ChoiceField(choices=[], required=False)
       
    def __init__(self, *args, **kwargs):
        super(PretestUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        if self.initial['users']:
            self.fields['account_selector'].choices = [(' ','--')] + [(i.id, str(i.first_name + ' ' + i.last_name + ', ' + i.email)) for i in self.initial['users']]
            self.fields['account_selector'].label = 'Choose an examinee from a list of users that are part of your organization. (optional):'
        else:
            # accounts are loaded from google db. remove the selector from this form. google selector form is defined in html and javascript.
            del self.fields['account_selector']

    class Meta:
        model = PretestUser
        fields = ['account_selector', 'email', 'first_name', 'last_name', 'program_id']
        labels = {'email': 'Enter a valid email address for a pretest examinee.', 'program_id': 'Program ID (optional)'}


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


class PretestResponseGradeForm(ModelForm):
    class Meta:
        model = PretestQuestionResponse
        fields = ['score']