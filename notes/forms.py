# notes/forms.py
from django import forms

from .models import UserNote

class UserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        fields = ['text', 'creator', 'content_type', 'object_id']
        widgets = { 
            'creator': forms.HiddenInput(), 
            'content_type': forms.HiddenInput(), 
            'object_id': forms.HiddenInput() 
            }
