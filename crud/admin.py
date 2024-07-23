from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('id','product', 'get_category')
    ordering = ('product',)

    def get_category(self, obj):
        return obj.get_category_display()
    get_category.short_description = 'Categoría'

admin.site.register(Product,ProductAdmin)