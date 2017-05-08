# forms.py

from django import forms
from django.forms import ModelForm
from django.contrib.contenttypes.models import ContentType

from .models import SurveyQuestionResponse


class SurveyQuestionResponseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyQuestionResponseForm, self).__init__(*args, **kwargs)
        try:
            self.fields['response'] = self.initial['question'].get_input_widget()
        except Exception as e:
            return
    
    class Meta:
        model = SurveyQuestionResponse
        fields = ['user', 'content_type', 'object_id', 'response']
        widgets = {
            'pretestuser': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput()
        }