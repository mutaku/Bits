from django.db import models
from utils.handlers import Hasher

StatusChoices = (
		( 0 , 'Open'),
		( 1 , 'Closed'),
	)

class Bit(models.Model):
	
	user = models.CharField("Created by",max_length=30)
	url = models.CharField("Reachable URL",max_length=10,blank=True,editable=False)

	date = models.DateTimeField("Date created",auto_now_add=True,unique=True)
	modified = models.DateTimeField("Last modified",auto_now=True)
	
	title = models.CharField("Title",max_length=255)
	note = models.TextField("Note")
	
	status = models.IntegerField("Status",max_length=1,choices=StatusChoices,default=0)
	tag = models.CharField("Associated tag",max_length=25)
	
	def save(self, *args, **kwargs):
		if not self.url:
			self.url = Hasher(self.date.__str__()).sha1()[:10]
		super(Bit, self).save(*args, **kwargs)

	def __unicode__(self):
		return u"%s" % self.title

