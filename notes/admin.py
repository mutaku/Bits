from notes.models import Bit
from django.contrib import admin
from utils.handlers import Hasher

class bitAdmin(admin.ModelAdmin):

	list_fields = ['title','user','url']	
	search_fields = ['tag']
	list_filter = ['tag','status']
	
	def save_model(self,request,obj,form,change):
		if not obj.url:
			obj.url = Hasher(obj.date.__str__()).sha1()[:10]
		obj.save()								


admin.site.register(Bit,bitAdmin)
