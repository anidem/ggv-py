from django.db import models
from django.core.urlresolvers import reverse

class QuestionResponse(models.Model):
	text = models.TextField()

	def __unicode__(self):
		return self.text

class QuestionOption(models.Model):
	text = models.CharField(max_length=512)
	correct = models.BooleanField(blank=True)
	
	def __unicode__(self):
		return self.text

class AbstractQuestion(models.Model):
	text = models.TextField()
	display_order = models.IntegerField()

	def __unicode__(self):
		return self.text

	class Meta:
		abstract = True

class SimpleQuestion(AbstractQuestion):

	def get_absolute_url(self):
		return reverse('course', args=[str(self.id)])

class MultipleChoiceQuestion(AbstractQuestion):
	RADIO = 'radio'
	CHECK = 'checkbox'
	
	SELECTION_TYPES = (
		(RADIO, 'radio'),
		(CHECK, 'checkbox'),
	)

	select_type = models.CharField(max_length=24, choices=SELECTION_TYPES, default='radio')
	options = models.ManyToManyField(QuestionOption)
	
	def get_absolute_url(self):
		return reverse('course', args=[str(self.id)])
	
	def __unicode__(self):
		return self.text

