from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('get_solicitud_id', 'get_solicitud_name', 'get_solicitud_birthday', 'get_solicitud_phone',
    'get_solicitud_gender', 'get_solicitud_comuna')
    ordering = ('solicitud',)

    def get_solicitud_id(self, obj):
        return obj.solicitud.id

    get_solicitud_id.short_description = 'ID USUARIO'  # Nombre de la columna en el admin

    def get_solicitud_name(self, obj):
        return f"{obj.solicitud.name} {obj.solicitud.last_name}"

    get_solicitud_name.short_description = 'Nombre'  # Nombre de la columna en el admin

    def get_solicitud_birthday(self, obj):
        return obj.solicitud.birthday

    get_solicitud_birthday.short_description = 'Fecha de Nacimiento'  # Nombre de la columna en el admin

    def get_solicitud_phone(self, obj):
        return obj.solicitud.phone_number

    get_solicitud_phone.short_description = 'Teléfono'  # Nombre de la columna en el admin

    def get_solicitud_gender(self, obj):
        return obj.solicitud.gender

    get_solicitud_gender.short_description = 'Género'  # Nombre de la columna en el admin

    def get_solicitud_comuna(self, obj):
        return obj.solicitud.comuna

    get_solicitud_comuna.short_description = 'Comuna'  # Nombre de la columna en el admin

admin.site.register(User, UserAdmin)
