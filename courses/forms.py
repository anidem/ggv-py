# courses/forms.py

from django import forms

from .models import Course


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['control_worksheet_results']
        labels = {
            'control_worksheet_results': 'Turn this on to restrict access to worksheet results when students complete a worksheet. ',
        }
