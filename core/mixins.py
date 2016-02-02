# core/mixins.py
from django.core.exceptions import PermissionDenied, ImproperlyConfigured

from guardian.shortcuts import get_perms

from courses.models import Course


class AccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """
        Permission checks here rely on session variables user_courses and user_lessons
        to make checks without hitting database.
        """
        if self.request.user.is_staff:
            course_access = True
            return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)

        course_access = self.kwargs[
            'crs_slug'] in self.request.session['user_courses']

        if not course_access:
            # early exit -- user accessing non assigned course
            raise PermissionDenied

        if self.access_object == 'lesson':
            course_access = self.get_object().id in self.request.session[
                'user_lessons']

        elif self.access_object == 'activity':
            course_access = self.lesson.id in self.request.session[
                'user_lessons']

        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)


class GGVUserViewRestrictedAccessMixin(object):
    """
    Intended to limit access to requested content to users that are either staff or
    have indicated privileges for the requested course.
    This mixin requires a crs_slug keyword argument in request.

    Requires CBV property required_privileges (as a list) to be set in requesting VIEW
    required_privileges = ['access', 'instructor', 'manage']

    Expected object type: User
    """

    def dispatch(self, *args, **kwargs):

        if self.request.user.is_staff:
            return super(GGVUserViewRestrictedAccessMixin, self).dispatch(*args, **kwargs)

        curr_course = Course.objects.get(slug=self.kwargs['crs_slug'])
        perms = get_perms(self.request.user, curr_course)

        # Does requestor have access to course (through crs_slug)?
        if not perms:
            raise PermissionDenied(self.request, 'access_forbidden.html')

        # Can managers see this content?
        if 'manage' in self.required_privileges and 'manage' in perms:
            return super(GGVUserViewRestrictedAccessMixin, self).dispatch(*args, **kwargs)

        # Can instructors see this content?
        if 'instructor' in self.required_privileges and 'instructor' in perms:
            return super(GGVUserViewRestrictedAccessMixin, self).dispatch(*args, **kwargs)

        # Can requesting user see this content (e.g., edit their own preferences)?
        if 'access' in self.required_privileges and self.get_object().id == self.request.user.id:
            return super(GGVUserViewRestrictedAccessMixin, self).dispatch(*args, **kwargs)

        raise PermissionDenied(self.request, 'access_forbidden.html')


class RestrictedAccessZoneMixin(object):

    """
    Intended to limit access to requested content to users with elevated privileges.
    User must be assigned 'manager' or 'instructor' permissions for requested course.

    Expected object type: Course
    """

    def dispatch(self, *args, **kwargs):
        """
        Permission checks here rely on object level permissions.
        """
        if self.request.user.is_staff:
            return super(RestrictedAccessZoneMixin, self).dispatch(*args, **kwargs)

        if type(self.get_object()) is Course:
            perms = get_perms(self.request.user, self.get_object())        
        else:
            perms = get_perms(self.request.user, self.course)
        
        if 'manage' in perms:
            return super(RestrictedAccessZoneMixin, self).dispatch(*args, **kwargs)

        if 'instructor' in perms:
            return super(RestrictedAccessZoneMixin, self).dispatch(*args, **kwargs)

        raise PermissionDenied


class PrivelegedAccessMixin(object):

    """
    Intended to set context variables indicating elevated privileges to view requested content.
    This mixin sets manager and/or instructor variables if such permissions are assigned to
    the user for a course.
    Expected object type: Course
    """

    def get_context_data(self, **kwargs):
        context = super(PrivelegedAccessMixin, self).get_context_data(**kwargs)
        course = self.get_object()
        user = self.request.user

        context['is_manager'] = user in course.manager_list() or user.is_staff
        context[
            'is_instructor'] = user in course.instructor_list() or user.is_staff

        return context


class CourseContextMixin(object):

    def get_context_data(self, **kwargs):
        """
        Intended to set context variable -- course -- based on request parameter crs_slug.
        Used in views to determine the course context for a request.

        Also sets context variable -- roles -- to provide the current role of the user in the course.
        This accesses the object permissions.
        """
        context = super(CourseContextMixin, self).get_context_data(**kwargs)
        try:
            context['course'] = Course.objects.get(
                slug=self.kwargs['crs_slug'])
            roles = get_perms(self.request.user, context['course'])

            if self.request.user.is_staff:
                context['role'] = 'GGV Staff'
                context['role_icon'] = 'fa fa-lock'

            elif 'manage' in roles:
                context['role'] = 'Course Manager'
                context['role_icon'] = 'fa fa-user-secret'

            elif 'instructor' in roles:
                context['role'] = 'Instructor'
                context['role_icon'] = 'fa fa-graduation-cap'

            elif 'access' in roles:
                context['role'] = 'Student'
                context['role_icon'] = 'fa fa-user'

        except Exception as e:
            pass
            # print e

        return context
