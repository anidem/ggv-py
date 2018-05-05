# maketestfixtures.py
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

from courses.models import *
from core import archiver
from core.models import *


class Command(BaseCommand):
    help = 'Overwrites and generates test data fixtures in core/fixtures from local db.'

    def handle(self, *args, **options):           	
    	self.serialize_base_data()
        self.serialize_user_data()

    """Alert: Be aware that this test data is generated from (ideally)
    a local development environment. If needed, a db update from production to local db can ensure replication of production data in test data.
    """
    def serialize_base_data(self):
        JSONSerializer =  serializers.get_serializer("json")
        jserializer = JSONSerializer()

        """Provides base data for content types and permissions"""
        f = './core/fixtures/django_contenttypes_and_perms.json'
        d = list(archiver.queryset_contenttypes())
        d += list(archiver.queryset_auth_permissions())
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All Site Pages"""
        f = './core/fixtures/sitepages.json'
        d = list(archiver.queryset_sitepages())
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All Site Messages"""
        f = './core/fixtures/sitemessages.json'
        d = list(archiver.queryset_sitemessages())
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All GGV Organizations"""
        f = './core/fixtures/orgs.json'
        d = archiver.queryset_ggvorgs()
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """Data for a set of specific courses:
            Admins Only & Developers Only
            Note that selected test data is relevant to these courses.
        """
        f = './core/fixtures/courses.json'
        d = list(Course.objects.filter(pk=1))
        d += list(Course.objects.filter(pk=18))
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All lessons"""
        f = './core/fixtures/lessons.json'
        d = archiver.queryset_lessons()
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All course_lesson pairs relevant to course data generated above."""
        f = './core/fixtures/course_lessons.json'
        d = list(CourseLesson.objects.filter(course__pk=1))
        d += list(CourseLesson.objects.filter(course__pk=18))
        # d = archiver.queryset_course_lesson()
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All sections"""
        f = './core/fixtures/sections.json'
        d = archiver.queryset_sections()
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All worksheets and related questions"""
        f = './core/fixtures/worksheets.json'
        d = list(archiver.queryset_questionsets())
        d += list(archiver.queryset_option_questions())
        d += list(archiver.queryset_text_questions())
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)

        """All slidestacks"""
        f = './core/fixtures/slidestacks.json'
        d = list(archiver.queryset_slidestacks())
        with open(f, 'w') as out:
            jserializer.serialize(d, indent=2, stream=out)
    
    def serialize_user_data(self):
        """Note: these selected user accounts are chosen relative to the 
        test course data generated above. These users are linked with 
        those courses with the exception of the orphan user.
        """

        # Student account active, non course member 462
        self.serialize_user_model(user_id=462, f='./core/fixtures/user_student_orphan.json')

        # Student account 397
        self.serialize_user_model(user_id=397, f='./core/fixtures/user_student.json')

        # Instructor account 2
        self.serialize_user_model(user_id=2, f='./core/fixtures/user_instructor.json')

        # Deactivated student account 743
        self.serialize_user_model(user_id=743, f='./core/fixtures/user_deactivated.json')

        # Unaccessed (unvalidated) account 924
        self.serialize_user_model(user_id=924, f='./core/fixtures/user_unvalidated.json')

        # Manager account 398
        self.serialize_user_model(user_id=398, f='./core/fixtures/user_manager.json')

        # Staff account 1
        self.serialize_user_model(user_id=1, f='./core/fixtures/user_staff.json')

        # Superuser account 1
        self.serialize_user_model(user_id=1, f='./core/fixtures/user_admin.json')

    def serialize_user_model(self, user_id=None, f=None):
        """Generates a fixture modeled from a specific user (id). 
            See function calls below for specific 'types' of user.
        """
        JSONSerializer =  serializers.get_serializer("json")
        jserializer = JSONSerializer()

        # User and GGVUser objects
        data = list(archiver.queryset_user_object(user_id))
        data += list(archiver.queryset_ggvuser_object(user_id))

        # User object permissions
        data += list(archiver.queryset_guardian_object_permissions(user_id))
        
        # User course access
        data += list(archiver.queryset_course_permissions(user_id))
        
        # User bookmarks, notifications, notes
        data += list(archiver.queryset_bookmarks(user_id))
        data += list(archiver.queryset_notifications(user_id))
        data += list(archiver.queryset_notes(user_id))
        
        #  User activity logs and attendance
        data += list(archiver.queryset_user_activity(user_id))
        data += list(archiver.queryset_user_attendance(user_id))
        
        # User worksheet data
        data += list(archiver.queryset_user_worksheet_completions(user_id))
        data += list(archiver.queryset_user_question_responses(user_id))
        with open(f, 'w') as out:
            jserializer.serialize(data, indent=2, stream=out)


