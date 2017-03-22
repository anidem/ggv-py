# utils.py

from django.views.generic import View, FormView, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

from .forms import TokenGeneratorForm
from .models import PretestAccount, PretestUser

class PretestCreateTokensView(FormView):
    template_name = 'pretest_token_generator.html'
    form_class = TokenGeneratorForm

    def dispatch(self, *args, **kwargs):
        
        if self.request.user.is_staff:
            return super(PretestCreateTokensView, self).dispatch(*args, **kwargs)
        messages.error(self.request, 'You do not appear to have valid access to this resource.', extra_tags='danger')
        return redirect('pretests:pretest_access_error') 

    def form_valid(self, form): 
    	data = form.cleaned_data
    	self.account = data['account']
    	for i in range(data['num_tokens']):
    		p = PretestUser(account=self.account)
    		p.save()

        return super(PretestCreateTokensView, self).form_valid(form)

    def get_success_url(self):
        success_url = reverse('pretests:pretest_user_list', args=[self.account.id], current_app=self.request.resolver_match.namespace)
        return success_url

    def get_context_data(self, **kwargs):
        context = super(PretestCreateTokensView, self).get_context_data(**kwargs)
        return context

class AccessErrorView(TemplateView):
    template_name = "pretest_access_error.html"

    def get_context_data(self, **kwargs):
        context = super(AccessErrorView, self).get_context_data(**kwargs)
        return context