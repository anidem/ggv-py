# questions/views.py
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin

from .models import QuestionSet, MultipleChoiceQuestion


class QuestionSetView(LoginRequiredMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        context['questions'] = MultipleChoiceQuestion.objects.filter(
            question_set=self.get_object().id)
        return context
