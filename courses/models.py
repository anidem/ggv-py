# courses/models.py

from operator import attrgetter

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from guardian.shortcuts import get_users_with_perms, get_perms, get_user_perms

from lessons.models import Lesson

ws_control_choices = (
    (False, 'OPTION 1: Students are allowed to immediately review the results after completing a worksheet.'),
    (True, 'OPTION 2:  Students are NOT allowed to immediately review the results after completing a worksheet.')
)

class GGVOrganization(models.Model):
    """
    An organization is a top level container for courses.
    """
    license_id = models.CharField(max_length=48, null=True)
    title = models.CharField(max_length=256)
    user_quota = models.IntegerField(default=0)
    manager_quota = models.IntegerField(default=0)
    instructor_quota = models.IntegerField(default=0)
    student_quota = models.IntegerField(default=0)
    quota_start_date = models.DateField()
    quota_end_date = models.DateField(null=True)
    business_contact_email = models.EmailField()
    business_contact_phone = models.CharField(max_length=12)

    def student_report(self, scope='all'):
        courses = self.organization_courses.all()
        rows = []
        for i in courses:
            rows.append(i.student_report(scope))
        return rows

    def licensed_user_list(self):
        users = []
        for course in self.organization_courses.all():
            for user in course.licensed_users():
                users.append(user[0])
        users = list(set(users))
        return users

    def licenses_in_use(self, scope=None):
        tag = ''
        if not scope:
            courses = self.organization_courses.all()
        else:
            try:
                tag = CourseTag.objects.get(pk=scope)
            except:
                pass
            
            courses = [t.course for t in TaggedCourse.objects.filter(tag=tag)]
        
        licensesd = {"active":{}, "unvalidated":{}}
        manager_count = 0
        instructor_count = 0
        student_count = 0
        unvalidated_count = 0
        for course in courses:
            for course_user in course.licensed_users():
                user_obj, course_obj, perms = course_user
                
                if user_obj.is_active:
                    status = 'active'
                else:
                    status = 'unvalidated'
                
                try:
                    licensesd[status][user_obj]['courses'].append(course_obj)
                    licensesd[status][user_obj]['perms'].update(perms)

                except KeyError:                   
                    licensesd[status][user_obj] = {'courses': [course_obj], 'perms': set(perms), 'status': user_obj.is_active}
                                      
                    if 'manage' in perms:
                        manager_count += 1
                    elif 'instructor' in perms:
                        instructor_count += 1
                    elif 'access' in perms:
                        student_count += 1
                    else:
                        unvalidated_count += 1

        # for k, v in licensesd.items():
        #     print k, len(v)
        #     for i, j in v.items():
        #         print '\t', i, j

        license_data = {
            'courses': courses,
            'tag_filter': tag,
            'active': licensesd['active'], 
            'unvalidated': licensesd['unvalidated'], 
            'count': manager_count + instructor_count + student_count + unvalidated_count, 
            'manager_count': manager_count,
            'instructor_count': instructor_count,
            'student_count': student_count,
            'unvalidated_count': unvalidated_count
        }
        
        return license_data

    def deactivated_users(self):
        courses = self.organization_courses.all()
        deactivated_list = {}
        for i in courses:
            deactivated_list[i] = i.deactivated_list()        

        return deactivated_list

    def instructor_list(self):
        courses = self.organization_courses.all()
        instructors = []
        for i in courses:
            instructors.extend(i.instructor_list())
        return instructors

    def manager_list(self):
        courses = self.organization_courses.all()
        managers = []
        for i in courses:
            managers += i.manager_list()
        return managers

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Course(models.Model):

    """
    Courses are synonymous with a testing site.
    A course contains one or more lessons and has zero or more designated instuctors and zero or more students.
    """
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=128, unique=True)
    control_worksheet_results = models.BooleanField(default=False, choices=ws_control_choices)
    access_code = models.CharField(max_length=8, null=True, blank=True)
    ggv_organization = models.ForeignKey(GGVOrganization, models.PROTECT, null=True, related_name='organization_courses')
    is_active = models.BooleanField(default=True)
    # tag = models.ForeignKey(CourseTag, models.SET_NULL, null=True, related_name='tagged_courses')

    class Meta:
        permissions = (
            ('access', 'Access'),
            ('instructor', 'Instructor'),
            ('manage', 'Manager'),
        )
        ordering = ['ggv_organization', 'title']

    def member_list(self):

        return get_users_with_perms(self, attach_perms=True)

    def licensed_users(self):
        members = self.member_list()
        unvalidated = [(user, self, perms) for user, perms in members.items() if not perms and not user.social_auth.all()]
        students = [(user, self, perms) for user, perms in members.items() if 'access' in perms and not user.is_staff and not user.is_superuser and 'instructor' not in perms]
        instructors = [(user, self, perms) for user, perms in members.items() if 'instructor' in perms and not user.is_staff]
        managers = [(user, self, perms) for user, perms in members.items() if 'manage' in perms and not user.is_staff]

        return unvalidated + students + instructors + managers 

    def student_list_all(self, extra_details=None, sort_by='first_name', reverse_sort=False):
        # if extra_details:
        # return [{user: ActivityLog.objects.filter(user=user)} for user, perms
        # in self.member_list().items() if 'access' in perms]

        students = [user for user, perms in self.member_list().items() if not user.is_staff and not user.is_superuser and 'instructor' not in perms]
        return sorted(students, key=attrgetter(sort_by), reverse=reverse_sort)

    def student_list(self, extra_details=None, sort_by='first_name', reverse_sort=False):
        # if extra_details:
        # return [{user: ActivityLog.objects.filter(user=user)} for user, perms
        # in self.member_list().items() if 'access' in perms]

        students = [user for user, perms in self.member_list().items() if 'access' in perms and not user.is_staff and not user.is_superuser and 'instructor' not in perms]
        return sorted(students, key=attrgetter(sort_by), reverse=reverse_sort)

    def instructor_list(self):
        return [user for user, perms in self.member_list().items() if 'instructor' in perms and not user.is_staff]

    def manager_list(self):
        return [user for user, perms in self.member_list().items() if 'manage' in perms and not user.is_staff]

    def activated_list(self):
        [user for user, perms in self.member_list().items() if user.is_active]

    def deactivated_list(self):
        return [user for user, perms in self.member_list().items() if not perms and user.social_auth.all()]

    def unvalidated_list(self):
        return [user for user, perms in self.member_list().items() if not perms and not user.social_auth.all()]

    def lesson_list(self):
        return self.crs_lessons.all()

    def student_report(self, scope='all'):
        if scope == 'active':
            student_list = self.student_list()
        elif scope == 'deactivated':
            student_list = self.deactivated_list()
        elif scope == 'unvalidated':
            student_list = self.unvalidated_list()
        else:
            student_list = self.student_list_all()
        
        rows = []
        for i in student_list:
            time_on_site = 0
            for j in i.attendance.all():
                time_on_site = time_on_site + j.duration_in_secs
            hours = time_on_site / 3600
            mins = time_on_site % 3600 / 60
            
            try:
                g = i.ggvuser.program_id
            except:
                g = None

            row = [
                g, 
                i.first_name, 
                i.last_name, 
                i.username, 
                i.last_login, 
                i.date_joined, 
                self.title, 
                self.ggv_organization.title, 
                (str(hours) + ':' + str(mins)),
                i.is_active,
            ]
            rows.append(row)
        return rows

    def get_user_role(self, user):
        return get_perms(user, self)

    def get_edit_privilege(self, user):
        return 'instructor' in self.get_user_role(user)

    def check_membership(self, user_session):
        """
        Utilizes session variable set at user login
        """
        return self.slug in user_session['user_courses']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', args=[str(self.slug)])


class CourseLesson(models.Model):

    """
        This class is used rather than a ManyToManyField in Course.
        Although it is nearly identical in function it is defined here to be more explicit
    """

    course = models.ForeignKey(Course, related_name='crs_lessons')
    lesson = models.ForeignKey(Lesson, related_name='crs_courses')

    def __unicode__(self):
        return '%s (%s)' % (self.course.title, self.lesson.title)

    def get_absolute_url(self):
        return reverse('lesson', args=[str(self.course.slug), str(self.lesson.id)])


class CoursePermission(models.Model):

    """ This class maps users with courses. It also indicates the user role. """

    USER_ROLES = (
        ('manager', 'Manager'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )

    user = models.ForeignKey(User, related_name='user_course_permissions')
    course = models.ForeignKey(Course, related_name='course_permissions')
    role = models.CharField(
        max_length=48, choices=USER_ROLES, default='student')

    def __unicode__(self):
        return '%s %s (%s)' % (self.course, self.user, self.role)


class CourseTag(models.Model):

    """ 
        This class models a suborganization entry for a ggv organization
        object.  A suborg can be further defined with a subset of licenses
        assigned to a ggv organization account.
    """

    title = models.CharField(max_length=512, null=False, unique=True)
    display_order = models.IntegerField(default=0)
    manager_quota = models.IntegerField(default=0)
    instructor_quota = models.IntegerField(default=0)
    student_quota = models.IntegerField(default=0)    
    ggv_organization = models.ForeignKey(GGVOrganization, blank=True, related_name='organization_tags')

    def __unicode__(self):
        return '%s' % (self.title)

    class Meta:
        ordering = ['display_order', 'title']


class TaggedCourse(models.Model):
    course = models.ForeignKey(Course, related_name='tag')
    tag = models.ForeignKey(CourseTag, related_name='tagged')

    def __unicode__(self):
        return '%s' % (self.tag)

    class Meta:
        ordering = ['course']


class CourseGrader(models.Model):
    grader = models.ForeignKey(User, related_name='courses_to_grade')
    course = models.ForeignKey(Course, related_name='assigned_graders')


    def __unicode__(self):
        return '%s' % (self.grader)
