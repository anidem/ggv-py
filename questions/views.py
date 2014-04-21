# questions/views.py
from django.views.generic import DetailView, UpdateView, TemplateView, CreateView
from django.forms.models import modelformset_factory, inlineformset_factory
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


from braces.views import LoginRequiredMixin, CsrfExemptMixin

from core.mixins import AccessRequiredMixin, AccessCodeRequiredMixin

from .models import QuestionSet, SimpleQuestion, QuestionResponse
from .forms import QuestionSetForm, QuestionResponseForm


class QuestionSetView(LoginRequiredMixin, CsrfExemptMixin, AccessRequiredMixin, DetailView):
    model = QuestionSet
    template_name = 'act_worksheet.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionSetView, self).get_context_data(**kwargs)
        context['questions'] = QuestionSet.objects.questions(id=self.get_object().id)
        return context

    # def get(self, request, *args, **kwargs):
    #     pass

    def post(self, request, *args, **kwargs):
        for i in request.POST:
            if i != 'csrfmiddlewaretoken':
                resp = QuestionResponse()
                resp.user = request.user
                resp.item = SimpleQuestion.objects.get(pk=i[i.find('_')+1:])
                resp.response = request.POST[i]
                resp.save()

                print 'response %s -> %s' % (i, request.POST[i])


        return render(request, self.template_name, {'feedback': 'thanks'})

    def form_valid(self, form):
        pass
        # return HttpResponseRedirect(reverse('worksheet_score', args=(p.id,)))

    def form_invalid(self, form):
        pass
