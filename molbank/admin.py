from django.contrib import admin
from .models import molbank,status,allplates
# Register your models here.
#class molAdmin(admin.ModelAdmin):
#	list_display = ('ID',)
from django.contrib.auth.models import Permission
admin.site.register(Permission)
admin.site.register(molbank)
admin.site.register(status)
admin.site.register(allplates)

