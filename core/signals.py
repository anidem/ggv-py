# core/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from guardian.shortcuts import get_objects_for_user


# @receiver(user_logged_in)
# def init_session(sender, **kwargs):
# 	request = kwargs['request']
# 	user = kwargs['user']
# 	# courses = user.course_membership.values_list('id', flat=True)
# 	courses = get_objects_for_user(user, 'view_course', Course).values_list('id', flat=True)
# 	request.session['user_courses'] = []
# 	for i in courses:
# 		request.session['user_courses'].append(i)

# 	print request.session['user_courses']
