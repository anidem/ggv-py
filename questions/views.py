# questions/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView

from .models import QuestionSet, MultipleChoiceQuestion


class QuestionSetView(DetailView):
    model = QuestionSet
    template_name = 'act_worksheet.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        context['questions'] = MultipleChoiceQuestion.objects.filter(
            question_set=self.get_object().id)
        return context
