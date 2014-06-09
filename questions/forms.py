# questions/forms.py
from django import forms
from django.forms import ModelForm, CharField, MultipleChoiceField
from .models import QuestionResponse

class QuestionPostForm(ModelForm):
    correct = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(QuestionPostForm, self).__init__(*args, **kwargs)
        try:
            initial_data = kwargs.pop('initial')
            initial_options = initial_data['options']
            intial_question = initial_data['question_text']
            initial_check = initial_data['correct']

            if initial_options:
                self.fields['response'].widget = forms.RadioSelect(choices=initial_options)
                   
            self.fields['response'].label = intial_question
            self.fields['correct'].value = initial_check        
        except:
            pass        

    class Meta:
        model = QuestionResponse
        fields = ['response', 'question_type', 'question_id', 'correct']
        widgets = { 
            'question_type': forms.HiddenInput(),
            'question_id': forms.HiddenInput()
            }