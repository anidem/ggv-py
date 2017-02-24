# pretests/mixins.py

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

from .models import PretestUser

class TokenAccessRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """
        Permission checks here rely on session variables.
        """
        if self.request.user.is_staff:
            return super(TokenAccessRequiredMixin, self).dispatch(*args, **kwargs)

        try:
        	token = self.request.session['pretester_token']
        	self.pretestuser = PretestUser.objects.get(access_token=token)
        
        except:
            messages.error(self.request, 'You will need provide your credentials again.', extra_tags='danger')
            return redirect('pretests:pretest_home')

        return super(TokenAccessRequiredMixin, self).dispatch(*args, **kwargs)