from django.contrib import admin
from .models import Solicitud, Comuna

# Register your models here.
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'last_name')
    ordering = ('last_name',)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id','comuna')
    ordering = ('comuna',)

admin.site.register(Solicitud,SolicitudAdmin)
admin.site.register(Comuna,ComunaAdmin)