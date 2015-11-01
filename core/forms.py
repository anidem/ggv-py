# core/forms.py
from django import forms
from django.forms import Form, ModelForm, ModelChoiceField, ChoiceField, BooleanField, CharField, EmailField

from django.contrib.auth.models import User

from core.models import GGVUser
from courses.models import Course
from .models import Bookmark

""" Administration/Management forms"""

LANG_CHOICES = (('english', 'English'), ('spanish', 'Spanish'))
ACCESS_CHOICES = (('access', 'Student Access'), ('instructor', 'Instructor Access'))
LABELS = {
    'language': 'Preferred language:',
    'program_id': 'Please enter a unique identifier for this user if your organization assigns ids to users:',
    'access_level': 'Select access level/account type:',
    'username': 'Username must be a valid email address managed by Google. Correspondence with user is made to this email account.',
    'is_active': 'Is activated? Uncheck this to deactivate user. User will not be able to access ggv.',
    'clean_logout': 'Google account security. Keep this CHECKED to safely log out of your Google account when signing out of GGV (recommended). UNCHECK this to stay logged in to your Google account after signing out of GGV.',
    'receive_notifications': 'Choose to receive notifications on student activity. (E.g., worksheet completions, bookmarking, etc.)',
    'receive_email_messages': 'Choose to receive email messages from the GGV system.'
    }


class GGVUsernameField(EmailField):
    label = 'Please enter a complete gmail address.'
    widget = forms.EmailInput()


class GgvUserAccountCreateForm(ModelForm):
    """
    Form designed for creating a new user account.

    Visibility: System admins, Managers
    """
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput())
    language = forms.ChoiceField(choices=LANG_CHOICES, label=LABELS['language'], required=False)
    perms = forms.ChoiceField(widget=forms.RadioSelect(), choices=ACCESS_CHOICES, label=LABELS['access_level'])
    username = forms.EmailField(widget=forms.EmailInput(), label=LABELS['username'])
    program_id = forms.CharField(label=LABELS['program_id'], required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'program_id',
                  'language', 'perms', 'course', 'is_active']
        widgets = {
            'is_active': forms.HiddenInput(),
        }


class GgvUserAccountUpdateForm(ModelForm):
    """
    Form designed for making changes to user account info.

    Visibility: System admins, Managers
    """
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    language = forms.ChoiceField(choices=LANG_CHOICES, label=LABELS['language'], required=False)
    perms = forms.ChoiceField(widget=forms.RadioSelect(), choices=ACCESS_CHOICES, label=LABELS['access_level'])
    username = forms.EmailField(widget=forms.EmailInput(), label=LABELS['username'])
    program_id = forms.CharField(label=LABELS['program_id'], required=False)
    receive_notify_email = forms.BooleanField(label=LABELS['receive_notifications'], required=False)
    receive_email_messages = forms.BooleanField(label=LABELS['receive_email_messages'], required=False)
    clean_logout = forms.BooleanField(label=LABELS['clean_logout'], required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'program_id', 'language', 'perms', 'course', 'receive_notify_email', 'receive_email_messages', 'clean_logout', 'is_active']
        labels = {'is_active': LABELS['is_active']}

""" User accessible settings. """


class GgvUserSettingsForm(ModelForm):
    """
    Form designed for non-student users to modify their personal preferences.

    Visibility: System admins, Managers, Instructors
    """
    language = forms.ChoiceField(choices=LANG_CHOICES, label=LABELS['language'], required=False)
    receive_notify_email = forms.BooleanField(label=LABELS['receive_notifications'], required=False)
    receive_email_messages = forms.BooleanField(label=LABELS['receive_email_messages'], required=False)
    clean_logout = forms.BooleanField(label=LABELS['clean_logout'], required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'language', 'clean_logout', 'receive_notify_email', 'receive_email_messages']
        labels = {
            'language_pref': 'Preferred language?',
            'clean_logout': 'Clean logout? (Logout of Google services when logging out of GGV. Recommended if you use GGV on public computers.)',
            'receive_notify_email': 'Receive student activity notifications in email?',
            'receive_email_messages': 'Receive emails from students?'
        }


class GgvUserStudentSettingsForm(ModelForm):
    """
    Form designed for student users to modify their preferences.

    Visibility: Students
    """
    language = forms.ChoiceField(choices=LANG_CHOICES, label=LABELS['language'], required=False)
    clean_logout = forms.BooleanField(label=LABELS['clean_logout'], required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'language', 'clean_logout']


class GgvEmailInstructors(Form):
    message = forms.CharField(
        widget=forms.Textarea,
        label='Use this text area to type your message to your instructor.',
        help_text='After pressing Send Message, your instructor will receive your message in their email.'
        )


class GgvEmailQuestionToInstructorsForm(Form):
    message = forms.CharField(
        widget=forms.Textarea,
        label='Use this text area to type your question for your instructor.',
        help_text='After pressing Send Message, your instructor will receive your message in their email.'
        )


class GgvEmailWorksheetErrorReportToStaffForm(Form):
    message = forms.CharField(
        widget=forms.Textarea,
        label='Use this text area to report a problem you encountered while using a worksheet. Examples include technical problems as well as problems with the question.',
        help_text='After pressing Send Message, GGV Staff will receive your message in their emails.'
        )


class GgvEmailStaffForm(Form):
    message = forms.CharField(
        widget=forms.Textarea,
        label='Use this text area to report a problem you encountered while using the GGV website. We gladly accept your error reports, comments, and feedback!',
        help_text='After pressing Send Message, GGV Staff will receive your message in their emails.'
        )


class BookmarkForm(ModelForm):

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


class PresetBookmarkForm(ModelForm):

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
