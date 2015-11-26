from django.test import TestCase

from django.contrib.auth.models import User

from questions.models import QuestionResponse, QuestionSet, OptionQuestion, TextQuestion


class WorksheetTestCase(TestCase):
    fixtures = [
        # 'contenttype_fixture.json',
        # 'user_fixture.json',
        'courses_fixture.json',
        'lessons_fixture.json',
        'worksheet_fixture.json',
        'checkbox_questions_fixture.json',
        'text_questions_fixture.json',
        'radio_questions_fixture.json',
        'question_responses_fixture.json',
        ]

    def setUp(self):
        user1 = User('u1').save()
        user2 = User('u2').save()
        user3 = User('u3').save()
        user4 = User('u4').save()




    def test_worksheet_scoring(self):
        """Worksheet get_user_score is tested."""
        ws = QuestionSet.objects.get(pk=1)

        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        user3 = User.objects.get(pk=3)
        user4 = User.objects.get(pk=4)

        self.assertEqual(ws.get_user_score(user1), 0.0)
        self.assertEqual(ws.get_user_score(user2), 0.0)
        self.assertEqual(ws.get_user_score(user3), 0.0)
        self.assertEqual(ws.get_user_score(user4), 0.0)

    def test_text_question_scoring(self):
        tq1 = TextQuestion.objects.get(pk=1)
        tq2 = TextQuestion.objects.get(pk=2)



    def test_radio_question_scoring(self):
        rq1 = OptionQuestion.objects.get(pk=1)


    def test_checkbox_question_scoring(self):
        cq1 = OptionQuestio.objects.get(pk=2)

