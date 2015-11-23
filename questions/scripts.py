from django.contrib.auth.models import User
from .models import *


# resps = QuestionResponse.objects.filter(user__id=36)

# for r in resps:
#     try:
#         r.iscorrect = r.content_object.check_answer(r)
#         r.save()
#     except TypeError:
#         print 'ERROR -- could not update correct answer for: ==> ', r.id

def populate_iscorrect_field():
    """
    Script used to calculate and update the correct/incorrect status of response. The result is added
    to the iscorrect field which as added to the response objects in november 2015.
    """
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


def update_worksheet_scores():
    """
    Script used to update a newly added field (score) to the UserWorksheetStatus model in
    november 2015. This script runs through each status object, computes the score and updates
    the score field for each status object.
    """
    users = User.objects.all().order_by('id')
    u = users[0].email
    for i in users:
        if u != i.email:
            u = i.email
            print 'Processing: ', u

        completions = UserWorksheetStatus.objects.filter(user=i)
        for j in completions:
            j.update_score()


def fix_malformed_multiple_choice_responses():
    """
    This script was created to fix malformed responses where a response to an option question (single response)
    was stored as a multiple response object in a list rather than a single string. There were only three responses
    objects that originally malformed.
    """
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
            # r.iscorrect = r.content_object.check_answer(r)
            # r.save()
            print 'FIX==>', r.response
