# core/models.py

from django.db import models
from django.contrib.auth.models import User

ACTIONS = (
    ('login', 'login'),
    ('logout', 'logout'),
    ('access', 'access'),
)

class ActivityLog(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField(max_length=32, choices=ACTIONS)
    message = models.CharField(max_length=64, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


"""
Probably need to have a custom manager for this model.
"""

