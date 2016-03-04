# core/models.py
import json
import calendar
from pytz import timezone
from datetime import datetime
from collections import OrderedDict

from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from courses.models import Course

tz = timezone(settings.TIME_ZONE)

ACTIONS = (
    ('login', 'login'),
    ('logout', 'logout'),
    ('access-question-text', 'access text question'),
    ('access-question-option', 'access multiple choice'),
    ('access-presentation', 'access presentation'),
    ('access-worksheet', 'access worksheet'),
    ('completed-worksheet', 'completed worksheet'),
)

BOOKMARK_TYPES = (
    ('remember', 'Review,Revisa'),
    ('todo', 'Need to Finish,Acabar'),
    ('started', 'Start,Comienza'),
    ('completed', 'Completed,Completado'),
    ('question', 'Question,Pregunta'),
    ('none', 'None,Borrar'),
)

ATTENDANCE_CODES = (
    (0, 'Online'),
    (1, 'Pretest'),
    (2, 'Official Test'),
    (3, 'Graduated'),
    (4, 'Dropped')
)


class GGVUser(models.Model):
    user = models.OneToOneField(User)
    program_id = models.CharField(max_length=32, null=True, blank=True, unique=True)
    language_pref = models.CharField(max_length=32, default='english', choices=(
        ('english', 'english'), ('spanish', 'spanish')))
    clean_logout = models.BooleanField(default=True)
    receive_notify_email = models.BooleanField(default=False)
    receive_email_messages = models.BooleanField(default=False)

    def attendance_by_month(self, year=None, month=None):
        try:
            if not year:
                curr = datetime.now(tz)                
            else:
                curr = datetime(int(year), int(month), 1)

            key = curr.strftime('%Y-%m')
            days = calendar.monthrange(curr.year, curr.month)
            attendance_list = [None] * days[1]    

            users_attendance = self.user.attendance.all().filter(datestr__startswith=key)
            
            for i in users_attendance:
                attendance_list[i.day_tz()-1] = i
        
        except Exception as e:
            attendance_list = []


        return attendance_list


    def attendance_full_listing(self):
        attendance_list = OrderedDict()
        for i in self.user.attendance.all().order_by('-datestamp'):
            d = i.datestamp.astimezone(tz).date() # .strftime('%b %Y')  # Creating a printable key for template rendering
            key = (d.year, d.month)
            if key not in attendance_list:
                attendance_list[key] = self.attendance_by_month(i.year_tz(), i.month_tz())

        return attendance_list

    def __unicode__(self):
        return self.user.username


class AttendanceTracker(models.Model):
    """
    Purpose is to maintain a separate record of attendance for each user. Important to
    note that these objects are created as a result of an ActivityLog save event. The datestr
    field is a shortcut for representing timezone aware date string based on datestamp

    datastamp is a UTC timestamp copied from activity log

    datestr is a date string in the format YYYY-MM-DD. When computed, the datestr represents
    a timezone aware date based on datestamp

    user and datestr must be unique together.

    The only editable/updatable field should be code.
    """

    user = models.ForeignKey(User, related_name='attendance')
    datestamp = models.DateTimeField()
    datestr = models.CharField(max_length=10, default='')
    code = models.PositiveIntegerField(choices=ATTENDANCE_CODES, default=0)

    def month_tz(self):
        return self.datestamp.astimezone(tz).month

    def day_tz(self):
        return self.datestamp.astimezone(tz).day

    def year_tz(self):
        return self.datestamp.astimezone(tz).year

    def __unicode__(self):
        return self.datestamp.astimezone(tz).strftime('%Y-%m-%d')

    class Meta:
        ordering = ['user', 'datestamp']
        unique_together = (('user', 'datestr'),)


class ActivityLog(models.Model):
    """
    Purpose is to maintain a log entry when a user logs in, logs out, accesses a worksheet,
    completes a worksheet, and accesses a presentation.
    """

    user = models.ForeignKey(User, related_name='activitylog')
    action = models.CharField(max_length=32, choices=ACTIONS)
    message = models.CharField(max_length=512, null=True, blank=True)
    message_detail = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def as_dict(self, course=None, exclusions=[]):
        from questions.models import QuestionSet, UserWorksheetStatus
        from slidestacks.models import SlideStack
        if self.action in exclusions:
            return None
        e = {
            'activity': self, 
            'report_url': self.message, 
            'event_time': self.timestamp_tz(), 
            'course': course, 
            'event_target': None, 
            'score': None
        }
        event_target_id = None
        try:
            activity_info = [j for j in self.message.split('/ggv/')[1].split('/')]
            event_target_id = activity_info[2]
        except:
            pass
        
        if self.action == 'completed-worksheet' or self.action == 'access-worksheet':
            try:
                worksheet = QuestionSet.objects.get(pk=event_target_id)
                e['event_target'] = worksheet 
                
                status = UserWorksheetStatus.objects.filter(user__id=self.user.id).get(completed_worksheet=worksheet)
                if status:
                    e['score'] = status.score
                    e['report_url'] = reverse('worksheet_user_report', args=[course.slug, worksheet.id, self.user.id])
                
            except Exception as exp:
                pass  # malformed log message or non-existent objects -- proceed silently...

        elif self.action == 'access-presentation':
            try:
                e['event_target'] = SlideStack.objects.get(pk=event_target_id)
            except Exception as exp:
                pass

        return e

    def timestamp_tz(self):
        return self.timestamp.astimezone(tz)

    def __unicode__(self):
        return self.timestamp.astimezone(tz).strftime('%b %d, %Y %-I:%M %p')

    def save(self, *args, **kwargs):
        super(ActivityLog, self).save(*args, **kwargs)
        """
        If an attendance tracker object does not exist for this ActivityLog object day
        then create a new attendance tracker object with object.user, object.date, object.datestr, object.code
        """
        try:
            a = AttendanceTracker( 
                user=self.user, 
                datestamp=self.timestamp, 
                datestr=self.timestamp.astimezone(tz).strftime('%Y-%m-%d'))
            a.save()
        
        except IntegrityError as e:
            # Attendance object already created for current day.
            pass

    class Meta:
        ordering = ['user', '-timestamp']


class Bookmark(models.Model):
    mark_type = models.CharField(
        max_length=32, choices=BOOKMARK_TYPES, default='none')
    creator = models.ForeignKey(User, related_name="bookmarker")
    content_type = models.ForeignKey(ContentType, related_name="bookmarks")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    course_context = models.ForeignKey(Course, null=True, blank=True)

    def notify_text(self):

        if str(self.content_type) in ['option question', 'text question']:
            target_url = self.content_object.get_sequence_url(self.course_context)
        else:
            target_url = self.content_object.get_absolute_url(crs_slug=self.course_context.slug)

        text = '%s %s bookmarked (%s) %s' % (self.creator.first_name, self.creator.last_name, self.mark_type, target_url)
        return text

    def __unicode__(self):
        return self.mark_type

    class Meta:
        unique_together = ('mark_type', 'creator', 'content_type', 'object_id', 'course_context')


class Notification(models.Model):
    user_to_notify = models.ForeignKey(User)
    context = models.CharField(max_length=128)
    event = models.CharField(max_length=512, blank=True, null=True)
    logdata = models.ForeignKey(ActivityLog, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    def get_event_dict(self):
        return json.loads(self.event)

    def __unicode__(self):
        return '%s, %s' % (self.event, self.logdata)


class SiteMessage(models.Model):
    message = models.TextField(default='Message from ggvinteractive.com here.')
    url_context = models.CharField(max_length=512, default='/', unique=True)
    show = models.BooleanField(default=True)

    def __unicode__(self):
        return self.message


class SitePage(models.Model):
    title = models.TextField()
    content = models.TextField()

    def __unicode__(self):
        return self.title




