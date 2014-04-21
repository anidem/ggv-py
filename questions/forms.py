# questions/forms.py
from django.forms import ModelForm
from django.forms.models import modelformset_factory

from .models import QuestionSet, SimpleQuestion, QuestionResponse

class QuestionSetForm(ModelForm):
    class Meta:
        model = QuestionSet

class QuestionResponseForm(ModelForm):
	class Meta:
		model = QuestionResponse
