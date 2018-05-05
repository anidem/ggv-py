from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from questions.models import QuestionResponse, QuestionSet, OptionQuestion, TextQuestion, UserWorksheetStatus


class WorksheetTestCase(TestCase):
    fixtures = [
        'fixture_worksheet_basic.json'        
        ]

    """ Worksheet listing info:
        id, display_order, type, response required
        1022 -1 text True
        1026 0 text True
        1023 1 text True
        1024 2 text True
        1025 2 text False
        12793 3 option True
        12794 4 option True
        12795 5 option True
    """
    def setUp(self):
        temp_student = User(username='temp_student', email="temp_student@ggv2.dev", password='1')
        temp_student.save()

    def test_worksheet_question_listing(self):
        user = User.objects.get(email='student@ggv2.dev')
        temp_student = User.objects.get(email='temp_student@ggv2.dev')
        ws = QuestionSet.objects.get(pk=143)
        questions = ws.get_ordered_question_list()
        questions_req = ws.get_ordered_question_list(required_questions=True)

        # Verify that questions returned match 8 for full listing, 7 if only listing required questions.
        self.assertEqual(len(questions), 8)
        self.assertEqual(len(questions_req), 7)

        # Verify that text question id 1023 is THIRD item in display order.
        self.assertEqual(questions[2].id, 1023)
        self.assertEqual(questions[2].get_question_type(), 'text')

        # Verify question count accessesors
        question_count = ws.get_num_questions()
        question_count_req = ws.get_num_questions(required_questions=True)
        self.assertEqual(question_count, 8)
        self.assertEqual(question_count_req, 7)

        # Verify that question id 1022 is at index 0
        q = ws.get_question_at_index(0)
        self.assertEqual(q['question'].id, 1022)
        self.assertEqual(q['index'], 0)

        # Verify that question id 12795 is at index 7 (last item)
        q = ws.get_question_at_index(7)
        self.assertEqual(q['question'].id, 12795)
        self.assertEqual(q['index'], 7)

        # Verify the upper bound in question list
        q = ws.get_question_at_index(8)
        self.assertEqual(q, None)

        # Verify that user has submitted all responses.
        q = ws.get_next_question(user)
        self.assertEqual(q, None)

        # Verify that temp user has not submitted any responses.
        # Should return question id 1022
        q = ws.get_next_question(temp_student)
        self.assertEqual(q['question'].id, 1022)
        self.assertEqual(q['index'], 1)

        # Verify no question precedes index 0
        q = ws.get_prev_question(0)
        self.assertEqual(q, None)

        # Verify question id 1022 precedes question at index 1
        q = ws.get_prev_question(1)
        self.assertEqual(q.id, 1022)

    def test_worksheet_scoring(self):
        """Worksheet get_user_score is tested."""
        user = User.objects.get(email='student@ggv2.dev')
        temp_student = User.objects.get(email='temp_student@ggv2.dev')
        ws = QuestionSet.objects.get(pk=143)

        self.assertEqual(ws.get_user_score(user), 100.0)
        self.assertEqual(ws.get_user_score(temp_student), 0.0)

        # Verify status score value 7/7 = 100.00
        status = UserWorksheetStatus.objects.filter(completed_worksheet=ws).get(user=user)
        self.assertEqual(status.score, 100.00)

        
    def test_text_question_scoring(self):
        user = User.objects.get(email='student@ggv2.dev')
        ws = QuestionSet.objects.get(pk=143)
        status = UserWorksheetStatus.objects.filter(completed_worksheet=ws).get(user=user)
        
        self.assertEqual(status.score, 100.00)

        # Verify score is updated to 6/7 = 85.714... after modifying a text question response.
        resp = QuestionResponse.objects.get(pk=133793) # currently 'blue' (correct)
        resp.response = 'green'
        resp.save()
        self.assertEqual(resp.iscorrect, False)

        # Verify status object score attribute is updated consistently
        status.update_score()
        self.assertEqual(ws.get_user_score(user), 85.71428571428571)
        self.assertEqual(status.score, 85.71428571428571)

        # Verify modification and update.
        resp.response = 'blue'
        resp.save()
        self.assertEqual(resp.iscorrect, True)

        # Verify status object score attribute is updated consistently
        status.update_score()
        self.assertEqual(ws.get_user_score(user), 100.00)
        self.assertEqual(status.score, 100.00)

    def test_radio_question_scoring(self):
        user = User.objects.get(email='student@ggv2.dev')
        ws = QuestionSet.objects.get(pk=143)
        status = UserWorksheetStatus.objects.filter(completed_worksheet=ws).get(user=user)
        
        # Modify a multiple choice (radio) response, verify score is 6/7 = 86.28...
        ctype = ContentType.objects.get_for_model(OptionQuestion)
        resp = QuestionResponse.objects.get(pk=133797)  # Correct response from user
        resp.response = '51795'  # pk to Option table -- incorrect
        resp.save()
        self.assertEqual(resp.iscorrect, False)

        status.update_score()
        self.assertEqual(ws.get_user_score(user), 85.71428571428571)
        self.assertEqual(status.score, 85.71428571428571)

    def test_checkbox_question_scoring(self):
        temp_student = User.objects.get(email='temp_student@ggv2.dev')
        ws = QuestionSet.objects.get(pk=143)
        ctype = ContentType.objects.get_for_model(OptionQuestion)

        self.assertEqual(ws.get_user_score(temp_student), 0.00)

        # Create a new multiple choice (checkbox) response, verify score is 1/7 = 14.28...
        resp = QuestionResponse(user=temp_student, 
            response="[51801, 51803]", # this is an Option pk list (the correct list) without json encoding.
            content_type=ctype,
            object_id=12795, 
            )
        resp.save()
        self.assertEqual(resp.iscorrect, True)
        self.assertEqual(ws.get_user_score(temp_student), 14.285714285714285)

        # Modify above response with an INCORRECT multiple choice (checkbox) response, verify score is updated to 0/7 = 00.00...
        resp = QuestionResponse(user=temp_student, 
            response="[51802, 51803]", # this is an Option pk list (incorrect list) without json encoding.
            content_type=ctype,
            object_id=12795, 
            )
        resp.save()
        self.assertEqual(resp.iscorrect, False)
        self.assertEqual(ws.get_user_score(temp_student), 0.0)

    def test_worksheet_status_update_score(self):
        user = User.objects.get(email='student@ggv2.dev')
        ws = QuestionSet.objects.get(pk=143)
        status = UserWorksheetStatus.objects.filter(completed_worksheet=ws).get(user=user)

        self.assertEqual(status.score, 100.00)
        
        # Verify modification and update.
        resp = QuestionResponse.objects.get(pk=133793)
        resp.response = 'green'
        resp.save()
        
        status.update_score()
        self.assertEqual(status.score, 85.71428571428571)




