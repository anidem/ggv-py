# data_archiver.py

"""
user data dump:

output to file:
----

user object

user activity log

user attendance

user worksheet completion status

user question responses

not archived:
----
bookmarks

notifications


"""

from django.core import serializers
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from guardian.models import UserObjectPermission

from courses.models import GGVOrganization, Course, CourseLesson, CoursePermission
from lessons.models import Lesson, Section
from questions.models import QuestionSet, OptionQuestion, TextQuestion, QuestionResponse, UserWorksheetStatus
from slidestacks.models import SlideStack
from core.models import GGVUser, Bookmark, Notification, SiteMessage, SitePage
from notes.models import UserNote 

#  BASE DATA
def queryset_contenttypes():
    try:
        query_set_obj = ContentType.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_auth_permissions():
    try:
        query_set_obj = Permission.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_sitepages():
    try:
        query_set_obj = SitePage.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_sitemessages():
    try:
        query_set_obj = SiteMessage.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_ggvorgs():
    try:
        query_set_obj = GGVOrganization.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_courses():
    try:
        query_set_obj = Course.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_lessons():
    try:
        query_set_obj = Lesson.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_course_lesson():
    try:
        query_set_obj = CourseLesson.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_sections():
    try:
        query_set_obj = Section.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_questionsets():
    try:
        query_set_obj = QuestionSet.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_option_questions():
    try:
        query_set_obj = OptionQuestion.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_text_questions():
    try:
        query_set_obj = TextQuestion.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_slidestacks():
    try:
        query_set_obj = SlideStack.objects.all()
        return query_set_obj
    
    except Exception as e:
        print e

#  END BASE DATA

#  USER DATA
def queryset_user_object(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = User.objects.filter(pk=u.id)
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_ggvuser_object(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = GGVUser.objects.filter(user=u.id)
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_guardian_object_permissions(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = UserObjectPermission.objects.filter(user=u)
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_course_permissions(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = CoursePermission.objects.filter(user=u.id)
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_user_activity(user_id=None):
    from core.models import ActivityLog, AttendanceTracker

    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = ActivityLog.objects.filter(user=u)
        return query_set_obj
    
    except Exception as e:
        print e

def queryset_user_attendance(user_id=None):
    from core.models import ActivityLog, AttendanceTracker

    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = AttendanceTracker.objects.filter(user=u)
        return query_set_obj
            
    except Exception as e:
        print e

def queryset_user_worksheet_completions(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = UserWorksheetStatus.objects.filter(user=u)
        return query_set_obj
            
    except Exception as e:
        print e

def queryset_bookmarks(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = Bookmark.objects.filter(creator=u)
        return query_set_obj
            
    except Exception as e:
        print e

def queryset_notifications(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = Notification.objects.filter(user_to_notify=u)
        return query_set_obj
            
    except Exception as e:
        print e

def queryset_notes(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = UserNote.objects.filter(creator=u)
        return query_set_obj
            
    except Exception as e:
        print e

def queryset_user_question_responses(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = QuestionResponse.objects.filter(user=u)
        return query_set_obj
    
    except Exception as e:
        print e

#  END USER DATA

#  RUN ALL QUERIES
def serialize_user_data(user_id=None, abs_root_dir=None):
    JSONSerializer =  serializers.get_serializer("json")
    jserializer = JSONSerializer()
    try:
        u = User.objects.get(pk=user_id)  
        fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '.json'
        master_queryset = []
        with open(fname, 'w') as out:
            master_queryset += list(SiteMessage.objects.all())
            master_queryset += list(SitePage.objects.all())
            master_queryset += list(queryset_contenttypes())
            master_queryset += list(queryset_auth_permissions())
            master_queryset += list(queryset_ggvorgs())
            master_queryset += list(queryset_courses())
            master_queryset += list(queryset_lessons())
            master_queryset += list(queryset_course_lesson())
            master_queryset += list(queryset_sections())
            master_queryset += list(queryset_questionsets())
            master_queryset += list(queryset_option_questions())
            master_queryset += list(queryset_text_questions())
            
            #  User data
            master_queryset += list(queryset_user_object(user_id))
            master_queryset += list(queryset_guardian_object_permissions(user_id))
            master_queryset += list(queryset_ggvuser_object(user_id))
            master_queryset += list(queryset_bookmarks(user_id))

            # master_queryset += list(queryset_notifications(user_id))

            master_queryset += list(queryset_notes(user_id))
            master_queryset += list(queryset_course_permissions(user_id))

            #  User activity logs and attendance

            master_queryset += list(queryset_user_activity(user_id))
            master_queryset += list(queryset_user_attendance(user_id))

            # User worksheet data

            master_queryset += list(queryset_user_worksheet_completions(user_id))
            master_queryset += list(queryset_user_question_responses(user_id))

            jserializer.serialize(master_queryset, indent=2, stream=out)
    
    except Exception as e:
        print 'Serialization error.'
        print type(e)
        print e.args  




