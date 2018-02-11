# core/forms.py
from django import forms
from django.forms import Form, ModelForm, ModelChoiceField, ChoiceField, BooleanField, CharField, EmailField, ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.models import User

from core.models import GGVUser, AttendanceTracker, GGVAccountRequest, SitePage
from courses.models import Course
from .models import Bookmark

""" Administration/Management forms"""

LANG_CHOICES = (('english', 'English'), ('spanish', 'Spanish'))
ACCESS_CHOICES = (('access', 'Student Access'), ('instructor', 'Instructor Access'))
LABELS = {
    'pretesters': 'Pretest Users who have completed pretests and are ready to begin using the GGV Curriculum',
    'language': 'Preferred language:',
    'program_id': 'Please enter a unique identifier (maximum 32 numbers or letters) for this user if your organization assigns ids to users. This is optional. A default identifier will be generated if one is not specified.<br><br>Program ID',
    'access_level': 'Select access level/account type:',
    'username': 'Users are identified by their gmail address/account. Please enter the user\'s complete email address. Organizations that use gmail as a service are considered valid gmail accounts.<br><br>Email',
    'is_active': 'Is activated? Uncheck this to deactivate user. User will not be able to access ggv.',
    'clean_logout': 'Google account security. Keep this CHECKED to ensure that this Google account is safely logged out of the browser. This is recommended. UNCHECK to ensure that this Google account remains active in the browser after signing out of GGV.',
    'receive_notifications': 'Choose to receive notifications on student activity. (E.g., worksheet completions, bookmarking, etc.)',
    'receive_email_messages': 'Choose to receive email messages from the GGV system.',
    'note': 'Specify a reason or other info regarding this account request (Optional).',
    'user_note': 'Enter an initial message to relay to the new user (student) when they are notified of their account status. (Optional).'
    }


class GGVUsernameField(EmailField):
    label = 'Please enter a complete gmail address or valid gmail account address.'
    widget = forms.EmailInput()


class GgvUserAccountCreateForm(ModelForm):
    """
    Form designed for creating a new user account. Form based on User model with additional
    custom fields defined as indicated.

    Visibility: System admins, Managers
    """

    account_selector = forms.ChoiceField(choices=[(' ','--')], required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput())
    language = forms.ChoiceField(choices=LANG_CHOICES, label=LABELS['language'], required=False)
    perms = forms.ChoiceField(widget=forms.RadioSelect(), choices=ACCESS_CHOICES, label=LABELS['access_level'])
    username = forms.EmailField(widget=forms.EmailInput(), label=LABELS['username'])
    program_id = forms.CharField(label=LABELS['program_id'], required=False)
    user_note = forms.CharField(widget=forms.Textarea, label='Additional information sent to user in their activation email.', required=False)

    def __init__(self, *args, **kwargs):
        super(GgvUserAccountCreateForm, self).__init__(*args, **kwargs)

        if self.initial['users']:  # This list is initialized in the calling view.          
            self.fields['account_selector'].choices = [(' ','--')] + [(i.id, unicode(i.first_name + u' ' + i.last_name + u', ' + i.email)) for i in self.initial['users']]
            self.fields['account_selector'].label = 'Select user information from a list of users who have completed their pretests. (optional):'

    def clean(self):
        data = super(GgvUserAccountCreateForm, self).clean()
        ggvorg = data['course'].ggv_organization
        user_licenses_used = ggvorg.licenses_in_use()
        if user_licenses_used['count'] >= ggvorg.user_quota:
            
            raise ValidationError('Number of user licenses for this organization has been exceeded. Additional users cannot be added. Consider deactivating old accounts to free up licenses for new users.', code='quota_exceeded')        

        return data

    class Meta:
        model = User
        fields = ['account_selector', 'perms', 'username', 'first_name', 'last_name', 'program_id',
                  'language', 'course', 'is_active', 'user_note']
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

    def __init__(self, *args, **kwargs):
        course_obj = kwargs.pop('course_obj')
        super(GgvUserAccountUpdateForm, self).__init__(*args, **kwargs)

        self.fields['course'].queryset = course_obj.ggv_organization.organization_courses.all()
        
        # Don't show notification options if student.
        if 'instructor' not in kwargs['initial']['perms']:
            self.fields['receive_notify_email'].widget = forms.HiddenInput()
            self.fields['receive_email_messages'].widget = forms.HiddenInput()        

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'program_id', 'language', 'perms', 'course', 'receive_notify_email', 'receive_email_messages', 'clean_logout', 'is_active']
        labels = {'is_active': LABELS['is_active']}
        widgets = {
            'is_active': forms.HiddenInput(), 
        }


class GgvUserRequestAccountForm(ModelForm):
    account_selector = forms.ChoiceField(choices=[(' ','--')], required=False)

    def __init__(self, *args, **kwargs):
        super(GgvUserRequestAccountForm, self).__init__(*args, **kwargs)

        if self.initial['users']:  # This list is initialized in the calling view.          
            self.fields['account_selector'].choices = [(' ','--')] + [(i.id, unicode(i.first_name + u' ' + i.last_name + u', ' + i.email)) for i in self.initial['users']]
            self.fields['account_selector'].label = 'Select user information from a list of users who have completed their pretests. (optional):'
    
    class Meta:
        model = GGVAccountRequest
        fields = ['account_selector', 'email', 'first_name', 'last_name', 'program_id',
                  'course', 'note', 'user_note', 'requestor']
        widgets = {
            'requestor': forms.HiddenInput()
        }
        labels = {
            'note': LABELS['note'],
            'user_note': LABELS['user_note'],
        }


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


class GgvEmailForm(Form):
    message = forms.CharField(
        widget=forms.Textarea,
        label='Use this text area to compose your email text.',
        help_text='Click Send Message to deliver your email message.'
        )
    

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


class GgvEmailDeactivationRequestForm(Form):
    deactivate = forms.CharField(
        widget=forms.Textarea,
        label='You are requesting that the site manager deactivate the following list of users.',
        help_text='After pressing Send Message, the site manager will receive your request in their email.'
        )


class GgvEmailActivationRequestForm(Form):
    message = forms.CharField(
        widget=forms.Textarea,
        label='You are requesting that the site manager activate the following list of users.',
        help_text='After pressing Send Message, the site manager will receive your request in their email.'
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


class AttendanceTrackerCreateForm(ModelForm):
    
    def form_valid(self):

        try:
            self.object = self.save(commit=False)
            self.object.full_clean()

        except Exception as e:
            pass

        return True

    class Meta:
        model = AttendanceTracker
        fields = ['user', 'datestamp', 'code']


class AttendanceTrackerUpdateForm(ModelForm):

    def form_valid(self):

        try:
            self.object = self.save(commit=False)
            self.object.full_clean()

        except Exception as e:
            pass

        return True

    class Meta:
        model = AttendanceTracker
        fields = ['code']


class SitePageCreateForm(ModelForm):

    class Meta:
        model = SitePage
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 70, 'class': 'editor'})
        }
