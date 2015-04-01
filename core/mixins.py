# core/mixins.py
from django.core.exceptions import PermissionDenied

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

        if not course_access:
            raise PermissionDenied

        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)

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

        perms = get_perms(self.request.user, self.get_object())
        if 'manage' in perms:
            return super(RestrictedAccessZoneMixin, self).dispatch(*args, **kwargs)

        if 'instructor' in perms:
            return super(RestrictedAccessZoneMixin, self).dispatch(*args, **kwargs)

        raise PermissionDenied
        # return super(RestrictedAccessZoneMixin, self).dispatch(*args, **kwargs)



class PrivelegedAccessMixin(object):

    """
    Intended to context variables indicating elevated privileges to view requested content.
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
        """
        context = super(CourseContextMixin, self).get_context_data(**kwargs)
        try:
            context['course'] = Course.objects.get(
                slug=self.kwargs['crs_slug'])
        except Exception as e:
            print e

        return context
