# courses/forms.py

from django import forms

from .models import Course



class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['control_worksheet_results']

        widgets = {'control_worksheet_results': forms.RadioSelect}

        labels = {'control_worksheet_results': 'How students view their worksheet results:'}
