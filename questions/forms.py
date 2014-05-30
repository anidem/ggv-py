# questions/forms.py
from django import forms
from django.forms import ModelForm, CharField, MultipleChoiceField, IntegerField
# from django.forms.models import BaseFormSet, BaseModelFormSet, modelformset_factory

# from crispy_forms.helper import FormHelper

from .models import QuestionSet, QuestionResponse

# class QuestionSetForm(BaseFormSet):

#     def __init__(self, questions, request=0,  *args, **kwargs):

#         self.questions = questions
#         super(QuestionSetForm, self).__init__(*args, **kwargs)
                
#         print 'initing formset==>%s' % request
#         self._construct_forms()

#     def _construct_forms(self):        
#         self.forms = []
#         print 'constructing forms==>%s' % self.questions
#         for i in xrange(len(self.questions)):
#             self.forms.append(self._construct_form(i, question_item=self.questions[i].id))


# class QuestionForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         try:
#             q = kwargs.pop('question_item') 
#         except:
#             q = None
        
#         super(QuestionForm, self).__init__(*args, **kwargs)
        
#         if q:
#             question = SimpleQuestion.objects.get(pk=q)
#             CHOICES = question.get_options().values_list('id', 'text')
#             self.fields['question'] = IntegerField(widget=forms.HiddenInput, label=question.id)
            
#             if question.select_type == 'radio':
#                 self.fields['response'] = MultipleChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=question.text)
#             elif q.select_type == 'checkbox':
#                 self.fields['response'] = MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple, label=question.text)
#             else:
#                 self.fields['response'] = CharField(label=question.text)
    
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         response = cleaned_data.get(response)
#         return cleaned_data

#     class Meta:
#         fields = ['question', 'response']

   






class QuestionPostForm(ModelForm):
    class Meta:
        model = QuestionResponse
        fields = ['response', 'question_type', 'question_id']
        widgets = { 'question_type': forms.HiddenInput()}


# class QuestionResponseFormDyno(ModelForm):
#     def __init__(self, worksheet, *args, **kwargs):
#         super(QuestionResponseFormDyno, self).__init__(*args, **kwargs)
#         question = SimpleQuestion.objects.get(pk=kwargs['question_id']) # get question to use with this response = passed from view?
#         print self.get_object()
#         question = self.object
#         self.queryset = QuestionSet.objects.questions(id=worksheet)
#         # self.fields['text'] = question.text
#         # if question.type == 'radio':
#         #   self.fields['options'] = MultipleChoiceField(queryset=question.get_options())
#         # elif question.type == 'checkbox':
#         #   self.fields['options'] = MultipleChoiceField(queryset=question.get_options())
#         # else:
#         #   self.fields['options'] = CharField()

#     class Meta:
#         model = SimpleQuestion

# # class QuestionResponseRadioForm(forms.Form):
# #   # widget = RadioSelect
# #   # choices = forms.MultipleChoiceField(CHOICES LIST)
# # class QuestionResponseCheckboxForm(forms.Form):
# #   # widget = CheckboxSelectMultiple
# #   # choices = forms.MultipleChoiceField(CHOICES LIST)
# # class QuestionResponseTextForm(forms.Form):
# #   # widget = TextInput
# #   # choices = forms.CharField(CHOICES LIST)
