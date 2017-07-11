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
    class Meta:
    	model = CourseGrader
    	fields = ['grader', 'course']
    	widgets = {'course': forms.HiddenInput}