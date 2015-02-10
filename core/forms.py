# core/forms.py
from django import forms

from .models import Bookmark

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['mark_type', 'creator', 'content_type', 'object_id', 'course_context']
        widgets = {
            'mark_type': forms.RadioSelect(),
            'creator': forms.HiddenInput(), 
            'content_type': forms.HiddenInput(), 
            'object_id': forms.HiddenInput(), 
            'course_context': forms.HiddenInput()
        }
        labels = {
            'mark_type': ''
        }

class PresetBookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['mark_type', 'creator', 'content_type', 'object_id', 'course_context']
        widgets = {
            'mark_type': forms.HiddenInput(),
            'creator': forms.HiddenInput(), 
            'content_type': forms.HiddenInput(), 
            'object_id': forms.HiddenInput(), 
            'course_context': forms.HiddenInput()
        }