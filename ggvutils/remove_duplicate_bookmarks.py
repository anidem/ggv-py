from core.models import *
from django.contrib.auth.models import User

types = [12, 13, 14, 15]

users = User.objects.all()
for user in users:
  for objtype in types:
    bks = user.bookmarker.all()
    bookmarks = bks.filter(content_type__id=objtype).order_by('object_id', '-id')
    uniques = {}
    for b in bookmarks:
        try:
          if uniques[b.object_id]:
            print 'duplicate', user, objtype, b.object_id, b.course_context_id
            # b.delete()
        except:
          uniques[b.object_id] = b

