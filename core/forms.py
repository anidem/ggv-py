# core/forms.py
from django import forms
from django.contrib.auth.models import User

from core.models import GGVUser
from courses.models import Course
from .models import Bookmark


class GgvUserCreateForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput())
    language = forms.ChoiceField(
        choices=(('english', 'English'), ('spanish', 'Spanish')),
        label='Preferred language:')
    perms = forms.ChoiceField(widget=forms.RadioSelect(),
                              choices=(('access', 'Student Access'), ('instructor', 'Instructor Access')), label="Select access level:")
    clean_logout = forms.BooleanField(
        label="Clean logout (uncheck to prevent complete google sign out):")
    username = forms.EmailField(
        widget=forms.EmailInput(), label='Please enter a complete gmail address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'language', 'perms', 'course', 'is_active', 'clean_logout']
        widgets = {
            'is_active': forms.HiddenInput(),
        }


class GgvUserSettingsForm(forms.ModelForm):

    class Meta:
        model = GGVUser
        fields = ['language_pref', 'clean_logout', 'receive_notify_email', 'receive_email_messages']


class GgvUserStudentSettingsForm(forms.ModelForm):

    class Meta:
        model = GGVUser
        fields = ['language_pref']


class GgvEmailForm(forms.Form):
    recipient_name = forms.CharField(required=True)
    recipient_email = forms.EmailField(required=True)
    senders_name = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)


class BookmarkForm(forms.ModelForm):

    def form_valid(self):

        try:
            self.object = self.save(commit=False)
            self.object.full_clean()

        except Exception as e:
            print e

        return True

    class Meta:
        model = Bookmark
        fields = ['mark_type', 'creator', 'content_type',
                  'object_id', 'course_context']
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
        fields = ['mark_type', 'creator', 'content_type',
                  'object_id', 'course_context']
        widgets = {
            'mark_type': forms.HiddenInput(),
            'creator': forms.HiddenInput(),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'course_context': forms.HiddenInput()
        }
