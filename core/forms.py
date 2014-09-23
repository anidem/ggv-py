# core/forms.py
from django.forms import ModelForm

from .models import UserNote

class UserNoteForm(ModelForm):
    
    class Meta:
        model = UserNote