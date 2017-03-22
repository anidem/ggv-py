# pretests/serializers.py

from django.core import serializers
from django.contrib.auth.models import User

from lessons.models import Lesson, Section
from questions.models import QuestionSet, TextQuestion, OptionQuestion, Option, QuestionResponse, UserWorksheetStatus

from .models import PretestAccount, PretestUser, PretestQuestionResponse, PretestUserCompletion


def generate_questions_fixtures():
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()

	""" A sample pretest worksheet containing all question types for Pretest Testing Exam...
		Note: this object (pk=159) may have been dumped. to create a dummy workhseet,
		create a new quiz in the system then set pk below to that quiz.
	"""
	ws = QuestionSet.objects.filter(pk=159)

	""" Related pretest lesson """
	ws_lesson = Lesson.objects.filter(pk=ws[0].lesson.id)

	""" Related pretest section """
	ws_section = Section.objects.filter(pk=ws[0].section.id)

	""" Related questions in pretest """
	option_questions = OptionQuestion.objects.filter(question_set=ws[0])
	options = Option.objects.filter(question__question_set=ws[0])
	text_questions = TextQuestion.objects.filter(question_set=ws[0])

	""" Related pretest completion status objects for pretestuser id of 5 at time of serialization """
	pretester = PretestUser.objects.filter(pk=5)
	with open('pretests/fixtures/fixture_pretesters.json', 'w') as out:
		jserializer.serialize(pretester, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	stat = PretestUserCompletion.objects.filter(completed_pretest=ws[0]).filter(pretestuser=pretester)
	with open('pretests/fixtures/fixture_pretest_completion_status.json', 'w') as out:
		jserializer.serialize(stat, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	""" Related user responses to worksheet """
	with open('pretests/fixtures/fixture_pretest_responses.json', 'w') as out:
	    
		for i in option_questions:
			responses = i.pretest_responses.filter(pretestuser=pretester)
			jserializer.serialize(responses, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
		for i in text_questions:
			responses = i.pretest_responses.filter(pretestuser=pretester)
			jserializer.serialize(responses, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	with open('pretests/fixtures/fixture_pretest_worksheet_lesson.json', 'w') as out:
	    jserializer.serialize(ws_lesson, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('pretests/fixtures/fixture_pretest_worksheet_section.json', 'w') as out: 
		jserializer.serialize(ws_section, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('pretests/fixtures/fixture_pretest_worksheet.json', 'w') as out:
	    jserializer.serialize(ws, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('pretests/fixtures/fixture_pretest_worksheet_text_questions.json', 'w') as out:
	    jserializer.serialize(text_questions, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('pretests/fixtures/fixture_pretest_worksheet_option_questions.json', 'w') as out:
	    jserializer.serialize(option_questions, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('pretests/fixtures/fixture_pretest_worksheet_options.json', 'w') as out:
	    jserializer.serialize(options, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)