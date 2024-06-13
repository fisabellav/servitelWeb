from django.contrib import admin
from .models import Solicitud, Comuna, SolicitudProducto

# Register your models here.
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'last_name')
    ordering = ('last_name',)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id','comuna')
    ordering = ('comuna',)

class SolicitudProductoAdmin(admin.ModelAdmin):
    list_display = ('get_solicitud_id', 'get_solicitud_name', 'product', 'quantity')
    ordering = ('solicitud',)

    def get_solicitud_id(self, obj):
        return obj.solicitud.id

    get_solicitud_id.short_description = 'ID de Solicitud'  # Nombre de la columna en el admin

    def get_solicitud_name(self, obj):
        return f"{obj.solicitud.name} {obj.solicitud.last_name}"

    get_solicitud_name.short_description = 'Nombre Solicitante'  # Nombre de la columna en el admin

admin.site.register(Solicitud,SolicitudAdmin)
admin.site.register(Comuna,ComunaAdmin)
admin.site.register(SolicitudProducto,SolicitudProductoAdmin)