from core.models import *
from django.contrib.auth.models import User

objs = {'stack': 12, 'ws': 13}

users = User.objects.all()
for user in users:
  bks = user.bookmarker.all()
  bookmarks = bks.filter(content_type__id=objs['ws']).order_by('object_id', '-id')
  uniques = {}
  for b in bookmarks:
    try:
      if uniques[b.object_id]:
        b.delete()
    except:
      uniques[b.object_id] = b
  bookmarks = bks.filter(content_type__id=objs['stack']).order_by('object_id', '-id')
  uniques = {}
  for b in bookmarks:
    try:
      if uniques[b.object_id]:
        b.delete()
    except:
      uniques[b.object_id] = b

