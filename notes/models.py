from django.db import models

StatusChoices = (
		( 0 , 'Open'),
		( 1 , 'Closed'),
	)

class Bit(models.Model):
	
	user = models.CharField(max_length=30)
	date = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	title = models.CharField(max_length=255)
	note = models.TextField()
	
	tags = models.ManyToManyField('Tags')
	
	hash = models.CharField(max_length=40)

	def __unicode__(self):
		return u"%s" % self.title

class Tags(models.Model):
	
	tagtext = models.CharField(max_length=50,unique=True)
		
	def __unicode__(self):		
		return u"%s" % self.tagtext

class Status(models.Model):
	
	switch = models.IntegerField(max_length=1,choices=StatusChoices,default=0)

	def __unicode__(self):
		return u"%s" % self.switch
