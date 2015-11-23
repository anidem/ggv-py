from django.contrib.auth.models import User
from .models import *


def fix_multiple_choice_responses():
    resps = QuestionResponse.objects.all().order_by('user')
    u = resps[0].user.email
    for r in resps:
        if u != r.user.email:
            u = r.user.email
            print 'Processing: ', u
        try:
            r.iscorrect = r.content_object.check_answer(r)
            r.save()
        except TypeError:
            print 'ERROR -- could not update correct answer for: ==> ', r.id


def fix_malformed_multiple_choice_responses():
    resps = QuestionResponse.objects.all().order_by('user')
    u = resps[0].user.email
    for r in resps:
        if u != r.user.email:
            u = r.user.email
            # print 'Processing: ', u, r.content_object.get_question_type(), r.response
        try:
            r.content_object.check_answer(r)

        except TypeError:
            print 'ERROR Processing:', u, r.content_object.get_question_type(), r.response
            rtemp = json.loads(r.response)[0]
            print 'FIXING==> ', r.id, rtemp
            r.response = int(rtemp)
            r.save()
            r.iscorrect = r.content_object.check_answer(r)
            r.save()
            print 'FIX==>', r.response


def update_worksheet_scores():
    users = User.objects.all().order_by('user')
    u = users[0].email
    for i in users:
        if u != i.email:
            u = i.email
            print 'Processing: ', u

        completions = UserWorksheetStatus.objects.filter(user=i)
        for j in completions:
            ws = j.completed_worksheet
            score = ws.get_user_score(i)
            j.score = score
            j.save()

