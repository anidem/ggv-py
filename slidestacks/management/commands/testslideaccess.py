# slidestacks/management/commands/testslideaccess.py
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import requests

from slidestacks.models import SlideStack

class Command(BaseCommand):
    """If running from crontab, then:
            VIRTUALENVPATH/python PROJECTPATH/manage.py testslideaccess
    """
    help = 'Verifies http access to all slidestack resources. Usage: testslideaccess'

    def handle(self, *args, **options):        
        try:
            base_url = settings.STACKS_URL

        except:
            raise CommandError('Check settings value for STACKS_URL')
    	
    	access_errors = self.test_production_access(base_url)
    	for i in access_errors:
    		self.stdout.write(self.style.ERROR(i))

    def test_production_access(self, base_url):
		"""Verifies that index.html in each ispring folder is accessible.
		Accessibility is tested against production server. Note the base_url 
		variable below.
		Note: The slidestacks db set should be updated to reflect current production
		references. E.g., If running locally, update local db from production db.
		"""

		slides = SlideStack.objects.all() 
		
		access_errors = []
		for i in slides:
			url = base_url+i.asset+'/index.html'
			r = requests.get(url)
			if r.status_code > 400:
				access_errors.append([r.status_code, i.pk, i.asset])
		return access_errors
