from lessons.models import *
from questions.models import *

srcs = range(93, 101)
srcq = []
for i in srcs:
    srcq.append(QuestionSet.objects.get(pk=i))

srcquestionsids = range(910, 918)
srcquestions = []
for i in srcquestionsids:
    srcquestions.append(TextQuestion.objects.get(pk=i))


science = Lesson.objects.get(pk=2)
social = Lesson.objects.get(pk=3)
writing = Lesson.objects.get(pk=4)

science_section = Section.objects.get(pk=17)
social_section = Section.objects.get(pk=14)
writing_section = Section.objects.get(pk=19)

# clone the source quiz, assign clone to new lesson and section

curs = 0
for source_quiz in srcq:
    source_quiz.pk = None
    source_quiz.save()  # creates a new object with auto generated id
    source_quiz.lesson = science
    source_quiz.section = science_section
    source_quiz.save()
    q = srcquestions[curs]
    q.pk = None
    q.save()
    q.question_set = source_quiz
    q.save()
    curs += 1

curs = 0
for source_quiz in srcq:
    source_quiz.pk = None
    source_quiz.save()  # creates a new object with auto generated id
    source_quiz.lesson = social
    source_quiz.section = social_section
    source_quiz.save()
    q = srcquestions[curs]
    q.pk = None
    q.save()
    q.question_set = source_quiz
    q.save()
    curs += 1

curs = 0
for source_quiz in srcq:
    source_quiz.pk = None
    source_quiz.save()  # creates a new object with auto generated id
    source_quiz.lesson = writing
    source_quiz.section = writing_section
    source_quiz.save()
    q = srcquestions[curs]
    q.pk = None
    q.save()
    q.question_set = source_quiz
    q.save()
    curs += 1
