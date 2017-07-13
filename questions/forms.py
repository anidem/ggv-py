# forms.py
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import QuestionResponse, OptionQuestion, TextQuestion, Option, QuestionSet, UserWorksheetStatus
# from filebrowser.widgets import FileInput, ClearableFileInput

import os
import json


class QuestionResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionResponseForm, self).__init__(*args, **kwargs)

        # question and user are assigned by the caller of the form
        # assigning to local variables for readability

        question = self.initial['question']
        user = self.initial['user']

        try:
            self.initial[
                'content_type'] = ContentType.objects.get_for_model(question)
            self.initial['object_id'] = question.id
            self.fields['response'] = question.get_input_widget()
        except:
            return

        # Check for previous response to question by user
        try:
            self.initial['response'] = question.user_response_object(user).json_response()
        except:
            pass

    # Override save method to handle previous responses.
    def save(self):
        submitted_form = super(
            QuestionResponseForm, self).save(commit=False)

        question = submitted_form.content_object
        user = submitted_form.user
         

        try:
            # Hack to strip whitespace from text question responses.
            # Review override clean method to do this...
            if question.input_size:
                submitted_form.response = submitted_form.response.strip()
        except:
            pass
            
        previous_response = question.user_response_object(user)
        
        # print "FORM==>:", submitted_form.response #json.dumps(self.cleaned_data['response'])

        if previous_response:
            previous_response.response = submitted_form.response
            previous_response.save()
            return previous_response
        else:
            try:
                if question.input_size and not question.auto_grade:
                    submitted_form.score = -1  # a new response is scored as -1 to indicate that it needs to be graded
            except:
                pass
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


class QuestionSetUpdateForm(ModelForm):

    def save(self):
        super(QuestionSetUpdateForm, self).save()
        try:
            pdfroot = settings.MEDIA_ROOT + '/'
            opts = pdfroot + self.instance.display_pdf.name + ' --dest-dir ' + pdfroot + 'pdf/'
            cmd = 'pdf2htmlEX ' + opts
            os.system(cmd)
        except:
            pass
        return self.instance
        
    class Meta:
        model = QuestionSet
        fields = ['title', 'lesson', 'section', 'instructions',
                  'display_order', 'display_pdf', ]
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 5, 'cols': 70, 'class': 'editor'})
        }


class OptionQuestionUpdateForm(ModelForm):

    def save(self):
        super(OptionQuestionUpdateForm, self).save()
        try:
            pdfroot = settings.MEDIA_ROOT + '/'
            opts = pdfroot + self.instance.display_pdf.name + ' --dest-dir ' + pdfroot + 'pdf/'
            cmd = 'pdf2htmlEX ' + opts
            print cmd
            os.system(cmd)
        except:
            pass
        return self.instance

    class Meta:
        model = OptionQuestion
        fields = ['question_set', 'display_text', 'response_required', 'content_area', 'extra_info', 'max_points', 'min_correct', 'display_order', 'input_select',
                  'display_image', 'display_pdf', 'display_key_file']
        widgets = {
            'display_text': forms.Textarea(attrs={'rows': 5, 'cols': 70, 'class': 'editor'}),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99}),
        }
        labels = {
            'input_select': 'Response type:',
            'display_image': 'Display an image <i class="fa fa-file-image-o fa-2x"></i>',
            'display_pdf': 'Display a PDF file <i class="fa fa-file-pdf-o fa-2x"></i>',
            'response_required': 'Users must respond? (Turn this off to only display content.) ',
            'display_key_file': 'Add answer key as PDF? <i class="fa fa-key fa-2x"></i> + <i class="fa fa-file-pdf-o fa-2x"></i>'
        }


class OptionUpdateForm(ModelForm):

    class Meta:
        model = Option
        fields = ['display_order', 'display_text', 'correct']
        widgets = {
            'display_text': forms.TextInput(attrs={'size': 40}),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99})
        }


OptionFormset = inlineformset_factory(
    OptionQuestion, Option, extra=4, form=OptionUpdateForm)


class TextQuestionUpdateForm(ModelForm):
    
    def save(self):
        super(TextQuestionUpdateForm, self).save()
        try:
            pdfroot = settings.MEDIA_ROOT + '/'
            opts = pdfroot + self.instance.display_pdf.name + ' --dest-dir ' + pdfroot + 'pdf/'
            cmd = 'pdf2htmlEX ' + opts
            os.system(cmd)
        except:
            pass
        return self.instance
        
    class Meta:
        model = TextQuestion
        fields = ['question_set', 'display_text', 'response_required', 'auto_grade', 'content_area', 'extra_info', 'max_points', 'min_correct', 'display_order', 'correct', 'input_size',
                  'display_image', 'display_pdf', 'response_required', 'display_key_file']
        widgets = {
            'display_text': forms.Textarea(attrs={'rows': 5, 'cols': 70, 'class': 'editor'}),
            'display_order': forms.NumberInput(attrs={'min': -99, 'max': 99}),
            'correct': forms.Textarea(attrs={'rows': 1, 'cols': 70})
        }
        labels = {
            'input_size': 'Size of text input area:',
            'display_image': 'Display an image <i class="fa fa-file-image-o fa-2x"></i>',
            'display_pdf': 'Display a PDF file <i class="fa fa-file-pdf-o fa-2x"></i>',
            'response_required': 'Users must respond? (Turn this off to only display content.) ',
            'display_key_file': 'Add answer key as PDF? <i class="fa fa-key fa-2x"></i> + <i class="fa fa-file-pdf-o fa-2x"></i>'
        }


class QuestionResponseGradeForm(ModelForm):
    class Meta:
        model = QuestionResponse
        fields = ['score', 'feedback']