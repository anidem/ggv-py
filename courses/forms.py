# courses/forms.py

from django import forms

from .models import Course


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['control_worksheet_results']
        labels = {
            'control_worksheet_results': 'CHECK this ON to restrict access to worksheet results after students have completed a worksheet. UNCHECK this to allow students to see their results after completing a worksheet.',
        }
