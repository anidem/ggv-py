# courses/forms.py

from django import forms

from .models import Course


class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['control_worksheet_results']
        labels = {
            'control_worksheet_results': 'Turn this on to restrict access to worksheet results after students have completed a worksheet. Turn this off to allow students to see their results after completing a worksheet.',
        }
