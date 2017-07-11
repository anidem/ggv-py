# courses/forms.py

from django import forms

from .models import Course, CourseGrader



class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['control_worksheet_results']

        widgets = {'control_worksheet_results': forms.RadioSelect}

        labels = {'control_worksheet_results': 'Control what happens after a student completes a worksheet:'}


class CourseUpdateGraderForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(CourseUpdateGraderForm, self).__init__(*args, **kwargs)
        # self.fields['grader'].choices = [(' ','--')] + [(i.id, str(i.first_name + ' ' + i.last_name + ', ' + i.email)) for i in self.initial['grader_list']]
        # if self.initial['users']:
        #     self.fields['account_selector'].choices = [(' ','--')] + [(i.id, str(i.first_name + ' ' + i.last_name + ', ' + i.email)) for i in self.initial['users']]

    class Meta:
    	model = CourseGrader
    	fields = ['grader', 'course']
    	widgets = {'course': forms.HiddenInput}