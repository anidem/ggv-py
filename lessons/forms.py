# forms.py
from django import forms


class StudentAccessForm(forms.Form):
    access_code = forms.CharField()

    def get_course(self):
        course = get_object_or_404(Course, access_code=self.access_code)
        pass
