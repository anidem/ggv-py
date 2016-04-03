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
from django.contrib.auth.models import User

from lessons.models import Lesson, Section
from questions.models import QuestionResponse, UserWorksheetStatus

def serialize_user_object(user_id=None, abs_root_dir=None):
    JSONSerializer =  serializers.get_serializer("json")
    jserializer = JSONSerializer()
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = User.objects.filter(pk=u.id)
        return query_set_obj

        # fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '.json'
    
    except Exception as e:
        print 'Serialization error.'
        print e

def serialize_user_activity(user_id=None):
    from core.models import ActivityLog, AttendanceTracker

    JSONSerializer =  serializers.get_serializer("json")
    jserializer = JSONSerializer()
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = ActivityLog.objects.filter(user=u)
        return query_set_obj

        # fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '-log.json'
    
    except Exception as e:
        print 'Serialization error.'
        print e

def serialize_user_attendance(user_id=None):
    from core.models import ActivityLog, AttendanceTracker

    JSONSerializer =  serializers.get_serializer("json")
    jserializer = JSONSerializer()
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = AttendanceTracker.objects.filter(user=u)
        return query_set_obj
        
        # fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '-attendance.json'
    
    except Exception as e:
        print 'Serialization error.'
        print e

def serialize_user_worksheet_completions(user_id=None):
    JSONSerializer =  serializers.get_serializer("json")
    jserializer = JSONSerializer()
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = UserWorksheetStatus.objects.filter(user=u)
        return query_set_obj
        
        # fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '-worksheet-completions.json'
    
    except Exception as e:
        print 'Serialization error.'
        print e


"""
deserialization integrity is not guaranteed here.
"""
def serialize_user_question_responses(user_id=None):
    try:
        u = User.objects.get(pk=user_id)
        query_set_obj = QuestionResponse.objects.filter(user=u)
        return query_set_obj
        # fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '-question-responses.json'
    
    except Exception as e:
        print 'Serialization error.'
        print e

def serialize_user_data(user_id=None, abs_root_dir=None):
    JSONSerializer =  serializers.get_serializer("json")
    jserializer = JSONSerializer()
    try:
        u = User.objects.get(pk=user_id)  
        fname = abs_root_dir + '/' + u.last_name.lower() + '-' + u.first_name.lower() + '.json'
        
        with open(fname, 'w') as out:
            query_set_obj = serialize_user_object(user_id)
            jserializer.serialize(query_set_obj, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

            query_set_obj = serialize_user_activity(user_id)
            jserializer.serialize(query_set_obj, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
            
            query_set_obj = serialize_user_attendance(user_id)
            jserializer.serialize(query_set_obj, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
            
            query_set_obj = serialize_user_worksheet_completions(user_id)
            jserializer.serialize(query_set_obj, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
            
            query_set_obj = serialize_user_question_responses(user_id)
            jserializer.serialize(query_set_obj, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
    
    except Exception as e:
        print 'Serialization error.'
        print e




