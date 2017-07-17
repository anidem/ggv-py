from django.contrib.auth.models import User
from lessons.models import Lesson
from core.models import ActivityLog


def activity_stat_worksheet(u, lesson_obj=None):
    """ Returns a lesson map mapping total number of worksheets and total user completions excludes pretest lessons
    """

    if not lesson_obj:  # get stats for all lessons
        lesson_worksheet_map = {lesson_obj: [lesson_obj.worksheets.all().count(), 0] for lesson_obj in Lesson.objects.all() if lesson_obj.title[-8:] != 'Pretests'}
        for i in u.completed_worksheets.all():
            lesson_worksheet_map[i.completed_worksheet.lesson][1] += 1
    
    else: # get stats by lesson object parameter
        lesson_worksheets = lesson_obj.worksheets.all().count()
        user_completed = u.completed_worksheets.all().filter(completed_worksheet__lesson=lesson_obj).count()
        lesson_worksheet_map = {lesson_obj: [lesson_worksheets, user_completed]}

    return lesson_worksheet_map

def activity_stat_slides(u, lesson_obj=None):
    """ Returns a presentation map mapping total number of presentations and total user views.
    """
    if not lesson_obj:  # get stats for all lessons
        lesson_stack_map = {i.title: [i.slidestacks.all().count(), 0] for i in Lesson.objects.all() if i.title[-8:] != 'Pretests'}
        events = u.activitylog.all().filter(action='access-presentation')
        stackviews = {i.message.rfind('/'): i.message_detail for i in events}
        for i, j in stackviews.items():
            # look up the associated lesson for the event and increment.
            lesson_stack_map[j][1] += 1
    
    else: # get stats by lesson object parameter
        lesson_stacks = lesson_obj.slidestacks.all().count()
        events = u.activitylog.all().filter(message_detail=lesson_obj.title).filter(action='access-presentation')
        # build dict {presentation id: lesson title}
        stackviews = {i.message.rfind('/'): lesson_obj.title for i in events}
        lesson_stack_map = {lesson_obj: [lesson_stacks, len(stackviews)]}

    return lesson_stack_map


u = User.objects.get(pk=269)  # test user
l = Lesson.objects.get(pk=1)  # test lesson

# print 'All lessons worksheet completions:'
# worksheets = activity_stat_worksheet(u)
# for i, j in worksheets.items(): print i,j

# print 'All lessons stack views'
# slideviews = activity_stat_slides(u)
# for i, j in slideviews.items(): print i,j

print '\n', l, 'worksheet completions'
worksheets = activity_stat_worksheet(u, l)
for i, j in worksheets.items(): print i,j

print '\n', l, 'stackviews'
slideviews = activity_stat_slides(u, l)
for i, j in slideviews.items(): print i,j

