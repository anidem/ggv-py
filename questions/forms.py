# forms.py
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import QuestionResponse, OptionQuestion, TextQuestion, Option

class QuestionResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionResponseForm, self).__init__(*args, **kwargs)

        # question and user are assigned by the caller of the form
        # assigning to local variables for readability

        question = self.initial['question']
        user = self.initial['user']

        self.initial[
            'content_type'] = ContentType.objects.get_for_model(question)
        self.initial['object_id'] = question.id
        self.fields['response'] = question.get_input_widget()

        # Check for previous response to question by user
        try:
            response = question.user_response_object(user).json_response()
            self.initial['response'] = response

            # Set user feedback info (correct or incorrect response)
            if question.check_answer(response):
                self.fields[
                    'response'].help_text = 'success'
            else:
                self.fields[
                    'response'].help_text = 'danger'

        except:
            pass

    # Override save method to handle previous responses.
    def save(self):
        submitted_form = super(
            QuestionResponseForm, self).save(commit=False)

        question = submitted_form.content_object
        user = submitted_form.user
        previous_response = question.user_response_object(user)

        try:
            # Hack to strip whitespace from text question responses.
            # Review override clean method to do this...
            if question.input_size:
                submitted_form.response = submitted_form.response.strip()
        except:
            pass

        if previous_response:
            previous_response.response = submitted_form.response
            previous_response.save()
        else:
            submitted_form.save()

        return submitted_form

    class Meta:
        model = QuestionResponse
        fields = ['user', 'content_type', 'object_id', 'response']
        widgets = {
            'user': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput()
        }

class OptionQuestionUpdateForm(ModelForm):
    class Meta:
        model = OptionQuestion
        fields = ['display_text', 'display_order', 'input_select', 'display_image']
        widgets = {
            'display_text': forms.Textarea(attrs={'rows': 5, 'cols': 70, 'class': 'editor'}),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99})
        }

class OptionUpdateForm(ModelForm):
    class Meta:
        model = Option
        fields = ['display_order', 'display_text', 'correct']
        widgets = {
            'display_text': forms.TextInput(attrs={'size': 40 }),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99})
        }

OptionFormset = inlineformset_factory(OptionQuestion, Option, extra=1, form=OptionUpdateForm)

class TextQuestionUpdateForm(ModelForm):
    class Meta:
        model = TextQuestion
        fields = ['display_text', 'display_order', 'correct', 'input_size', 'display_image']
        widgets = {
            'display_text': forms.Textarea(attrs={'rows': 5, 'cols': 70, 'class': 'editor'}),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99}),
            'correct': forms.Textarea(attrs={'rows': 1, 'cols': 70})
        }

