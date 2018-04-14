from django.test import TestCase

from .models import GGVOrganization, Course, CourseLesson, CoursePermission, \
	CourseTag, TaggedCourse, CourseGrader

# MODEL TESTS: ORGANIZATION
# class GGVOrganization(TestCase):
#     def setUp(self):
#     	s = datetime
#         GGVOrganization.objects.create(title="org_a", quota_start_date)
#         GGVOrganization.objects.create(title="org_b")

#     def test_ggvorg_license_expired(self):
#         """A ggv organization whose license quota is not expired."""
#         ggvorga = Animal.objects.get(title="lion")
#         self.assertEqual(ggvorga.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')



# MODEL TESTS: COURSE