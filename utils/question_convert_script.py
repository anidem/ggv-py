# Converts all questions in a worksheet from text to multiple choice. Can easily
# be modifed to go the other way or modified to convert 1 or more select questions.
# ALERT: THIS SCRIPT WILL DELETE DATA! Backup before attempting or modify to do a "dry run"

from questions.models import *
from utils.wsutil import convert_text_to_option

# UNCOMMENT AND MODIFTY THIS ACCORDINGLY
ws = QuestionSet.objects.get(pk=129)

# clear all status objects for the worksheet
for status in UserWorksheetStatus.objects.filter(completed_worksheet=ws):
  status.delete()

# Either retrieve all questions from a worksheet:
questions = ws.get_ordered_question_list()

# or specify pks for each question to convert:
# pks = []
# questions = []
# for i in pks:
#     questions.append(TextQuestion.objects.get(pk=i))


# clear all bookmarks for each question
for q in questions:
  for b in q.bookmarks.all():
    b.delete()

# clear all responses for each question
for q in questions:
  for r in q.responses.all():
    r.delete()

# convert all questions in worksheet (or in question list) from text to multiple choice
for q in questions:
  newq = convert_text_to_option(source_pk=q.id)
  print newq.get_question_type(), newq.question_set


