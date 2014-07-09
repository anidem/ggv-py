# questions/forms.py
from django import forms
from django.forms import ModelForm, CharField, MultipleChoiceField
from .models import QuestionResponse

class QuestionPostForm(ModelForm):
    correct = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        
        try:
            super(QuestionPostForm, self).__init__(*args, **kwargs)
            initial_data = kwargs.pop('initial')
            initial_options = initial_data['options']
            intial_question = initial_data['question_text']
            initial_check = initial_data['correct']

            if initial_options:
                self.fields['response'].widget = forms.RadioSelect(choices=initial_options)
            else:
                self.fields['response'].widget.attrs = {
                    'rows': '1',
                    'size': '5',
                    }
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

class MultipleChoiceQuestionForm(ModelForm):
    user = None
    correct = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(MultipleChoiceQuestionForm, self).clean()
        cleaned_data['user'] = self.user
        return cleaned_data

    # def __init__(self, *args, **kwargs):
    #     super(MultipleChoiceQuestionForm, self).__init__(*args, **kwargs)
    #     if self.initial:
    #         self.fields['response'].widget.choices = self.initial['choices']
    #         self.fields['response'].label = self.initial['question_prompt']
    #         self.user = self.initial['user']

    class Meta: 
        model = QuestionResponse
        fields = ['response', 'question_type', 'question_id', 'correct']
        widgets = {
                'response': forms.RadioSelect(),
                'question_type': forms.HiddenInput(),
                'question_id': forms.HiddenInput() 
            }

class ShortAnswerQuestionForm(ModelForm):
    user = None
    correct = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(ShortAnswerQuestionForm, self).clean()
        cleaned_data['user'] = self.user
        return cleaned_data

    # def __init__(self, *args, **kwargs):
    #     super(ShortAnswerQuestionForm, self).__init__(*args, **kwargs)
    #     self.fields['response'].label = self.initial['question_prompt']
    #     self.user = self.initial['user']

    class Meta:
        model = QuestionResponse

        fields = ['response', 'question_type', 'question_id', 'correct']
        widgets = { 
            'question_type': forms.HiddenInput(),
            'question_id': forms.HiddenInput()
            }