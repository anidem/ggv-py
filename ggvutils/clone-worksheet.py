from questions.models import *
from lessons.models import *

lesson = Lesson.objects.get(pk=)
section = Section.objects.get(pk=)

ws_ids = []

for w in ws_ids:
    worksheet = QuestionSet.objects.get(pk=w)
    questions = worksheet.get_ordered_question_list()
    worksheet.pk = None
    worksheet.save()
    worksheet.lesson = lesson
    worksheet.section = section
    worksheet.save()
    for q in questions:
        options = q.options.all()
        q.pk = None
        q.save()
        q.question_set = worksheet
        q.save()
        for o in options:
            o.pk = None
            o.save()
            o.question = q
            o.save()
