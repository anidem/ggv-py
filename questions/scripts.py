from django.contrib.auth.models import User
from .models import *

"""
System maintenance procedure jan 2 1016:
a. Repair response table with fix_response_fields().
b. Update response table iscorrect field with update_iscorrect_field()
c. Update worksheet score field with update_worksheet_scores()
d. Uncomment the update score procedure in QuestionResponse.save() method.
e. Recommit and pull to production.
"""


def fix_response_fields():
    """
    maintenance script that converts radio button responses and text responses to non-json encoded strings.
    Checkbox responses are designed to be stored as json encoded list. these must remain json encoded.
    """
    text_responses = QuestionResponse.objects.filter(content_type_id=14)
    print 'Text responses ==>', text_responses.count()
    count = 0
    for i in text_responses:
        try:
            i.response = json.loads(i.response)
            i.save()
            count = count + 1
        except:
            pass # Don't modify, response is not json encoded.

    print 'Decoded JSON strings ==>', count


    mc_responses = QuestionResponse.objects.filter(content_type_id=15)
    radio_responses = []
    for i in mc_responses:
        if i.content_object.input_select=='radio':
            radio_responses.append(i)

    print 'Radio responses ==>', len(radio_responses)

    count = 0
    for i in radio_responses:
        try:
            i.response = json.loads(i.response)
            i.save()
            count = count + 1
        except:
            pass  # Don't modify, response is not json encoded.

    print 'Decoded JSON strings ==>', count


def update_iscorrect_field():
    """
    Script used to calculate and update the correct/incorrect status of response. The result is added
    to the iscorrect field which was added to the response objects in november 2015.
    """
    resps = QuestionResponse.objects.all().order_by('user')
    u = 'blank'
    for r in resps:
        if u != r.user.email:
            u = r.user.email
            print 'Processing: ', u
        try:
            r.save()  # Saving updates iscorrect field
        except Exception as e:
            print e
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



