import requests

from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode

from .models import SlideStack



class SlideStackTestCase(TestCase):

	fixtures = ['lessons.json', 'sections.json', 'slidestacks.json']

	def test_production_index_access_all(self):
		"""Verifies that index.html in each ispring folder is accessible.
		Accessibility is tested against production server. Note the base_url 
		variable below.
		Note: The slidestacks-data fixture should be updated to reflect current
		references in the slidestack objects.
		"""
		base_url = settings.STACKS_URL

		slides = SlideStack.objects.all()
		print slides.count()
		access_errors = []
		for i in slides:
			url = base_url+i.asset+'/index.html'
			r = requests.get(url)
			if r.status_code > 400:
				access_errors.append([r.status_code, i.asset])

		for i in access_errors:
			print i
			
		self.assertEqual(len(access_errors), 0)

		


