# notes/forms.py
from django import forms

from .models import UserNote

class UserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        fields = ['text', 'creator', 'content_type', 'object_id', 'course_context']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
            'creator': forms.HiddenInput(), 
            'content_type': forms.HiddenInput(), 
            'object_id': forms.HiddenInput(), 
            'course_context': forms.HiddenInput()
        }
        labels = {
            'text': ''
        }
