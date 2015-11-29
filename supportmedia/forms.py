# forms.py
from django import forms
from django.forms import ModelForm

from .models import ExternalMedia


class UpdateExternalMediaForm(ModelForm):

    class Meta:
        model = ExternalMedia
        fields = ['title', 'instructions', 'lesson', 'section', 'display_order', 'media_link', 'media_embed']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 5, 'cols': 70, 'class': 'editor'}),
            'media_embed': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99}),
        }
        labels = {
            'media_link': 'Copy and paste the YouTube link here.',
            'media_embed': 'Copy and paste the YouTube embed code here.',
        }
