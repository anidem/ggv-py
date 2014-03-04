# questions/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView

from .models import MultipleChoiceQuestion, SimpleQuestion, QuestionOption

class MultipleChoiceQuestionDetailView(DetailView):
	model = MultipleChoiceQuestion
	# context_object_name = 'question'
	template_name = 'multiple_choice.html'

	def get_context_data(self, **kwargs):
		context = super(MultipleChoiceQuestionDetailView, self).get_context_data(**kwargs)
		context['options'] = self.get_object().options.all()
		return context

class MultipleChoiceQuestionCreateView(CreateView):
	model = MultipleChoiceQuestion
	template_name = 'multiple_choice_create.html'
	fields = ['text', 'options', 'select_type', 'display_order']

	def form_valid(self, form):
		return super(MultipleChoiceQuestionCreateView, self).form_valid(form)
