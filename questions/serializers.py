# serializers.py
# questions app serializer functions

from django.core import serializers
from django.contrib.auth.models import User

from lessons.models import Lesson, Section
from questions.models import QuestionSet, TextQuestion, OptionQuestion, Option, QuestionResponse, UserWorksheetStatus

def generate_user_fixtures():
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()

	""" A student user account """
	student_user_0 = User(username='student_0', email="temp_student_0@ggv2.dev", password='1')
	student_user_0.save()
	
	""" An instructor user account """
	instructor_user_0 = User(username='instructor_0', email='instructor_0@ggv2.dev', password='1')
	instructor_user_0.save()

	

	with open('core/fixtures/fixture_users.json', 'w') as out:
	    jserializer.serialize(User.objects.filter(username='student_0'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	    jserializer.serialize(User.objects.filter(username='instructor_0'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)


	student_user_0.delete()
	instructor_user_0.delete()

def generate_questions_fixtures():
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()

	""" A sample worksheet containing all question types ==> Demo Quiz
		Note: this object (pk=143) was dumped. to create a dummy workhseet,
		create a new quiz in the system then set pk to that quiz.
	"""
	ws = QuestionSet.objects.filter(pk=143)

	""" Related worksheet lesson """
	ws_lesson = Lesson.objects.filter(pk=ws[0].lesson.id)

	""" Related worksheet section """
	ws_section = Section.objects.filter(pk=ws[0].section.id)

	""" Related questions in worksheet """
	option_questions = OptionQuestion.objects.filter(question_set=ws)
	options = Option.objects.filter(question__question_set=ws)
	text_questions = TextQuestion.objects.filter(question_set=ws)

	""" Related worksheet status objects for user """
	stat = UserWorksheetStatus.objects.filter(completed_worksheet=ws).filter(user=user)
	with open('questions/fixtures/fixture_worksheet_status.json', 'w') as out:
		jserializer.serialize(stat, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	""" Related user responses to worksheet """
	with open('questions/fixtures/fixture_worksheet_responses.json', 'w') as out:
	    
		for i in option_questions:
			responses = i.responses.filter(user__id=12)
			jserializer.serialize(responses, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
		for i in text_questions:
			responses = i.responses.filter(user__id=12)
			jserializer.serialize(responses, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	with open('questions/fixtures/fixture_worksheet_lesson.json', 'w') as out:
	    jserializer.serialize(ws_lesson, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('questions/fixtures/fixture__worksheet_section.json', 'w') as out: 
		jserializer.serialize(ws_section, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('questions/fixtures/fixture_worksheet.json', 'w') as out:
	    jserializer.serialize(ws, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('questions/fixtures/fixture_worksheet_text_questions.json', 'w') as out:
	    jserializer.serialize(text_questions, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('questions/fixtures/fixture_worksheet_option_questions.json', 'w') as out:
	    jserializer.serialize(option_questions, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	with open('questions/fixtures/fixture_worksheet_options.json', 'w') as out:
	    jserializer.serialize(options, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)


	""" A worksheet containing text questions """
	# ws_text_questions = QuestionSet.objects.filter(pk=429)
	# text_questions = TextQuestion.objects.filter(question_set=ws_text_questions)
	# with open('questions/fixtures/fixture_text_questions.json', 'w') as out:
	#     jserializer.serialize(ws_text_questions, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	#     jserializer.serialize(text_questions, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	# """ A worksheet containing single select (radio) multiple choice questions """
	# ws_mc_questions_radio = QuestionSet.objects.filter(pk=422)
	# mc_options_radio = Option.objects.filter(question__question_set=ws_mc_questions_radio)
	# mc_questions_radio = OptionQuestion.objects.filter(question_set=ws_mc_questions_radio)

	# with open('questions/fixtures/fixture_mc_questions_radio.json', 'w') as out:
	#     jserializer.serialize(ws_mc_questions_radio, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	#     jserializer.serialize(mc_questions_radio, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	#     jserializer.serialize(mc_options_radio, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

	# """ A worksheet containing multiple select (checkbox) multiple choice questions """
	# ws_mc_questions_ckbox = QuestionSet.objects.filter(pk=556)
	# mc_options_ckbox = Option.objects.filter(question__question_set=ws_mc_questions_ckbox)
	# mc_questions_ckbox = OptionQuestion.objects.filter(question_set=ws_mc_questions_ckbox)
	
	# with open('questions/fixtures/fixture_mc_questions_ckbox.json', 'w') as out:
	#     jserializer.serialize(ws_mc_questions_ckbox, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	#     jserializer.serialize(mc_questions_ckbox, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
	#     jserializer.serialize(mc_options_ckbox, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)


def serialize_question_sets(fname='questions/fixtures/serialized_question_sets.json'):
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()
	with open(fname, 'w') as out:
	    jserializer.serialize(QuestionSet.objects.all().order_by('id'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

def serialize_text_questions(fname='questions/fixtures/serialized_text_questions.json'):
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()
	with open(fname, 'w') as out:
	    jserializer.serialize(TextQuestion.objects.all().order_by('id', 'display_order'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

def serialize_options(fname='questions/fixtures/serialized_options.json'):
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()
	with open(fname, 'w') as out:
	    jserializer.serialize(Option.objects.all().order_by('question', 'display_order'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

def serialize_option_questions(fname='questions/fixtures/serialized_option_questions.json'):
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()
	with open(fname, 'w') as out:
	    jserializer.serialize(OptionQuestion.objects.all().order_by('id', 'display_order'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)

def serialize_user_worksheet_status(fname='questions/fixtures/serialized_user_worksheet_status.json'):
	JSONSerializer =  serializers.get_serializer("json")
	jserializer = JSONSerializer()
	with open(fname, 'w') as out:
	    jserializer.serialize(UserWorksheetStatus.objects.all().order_by('completed_worksheet'), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, stream=out)
