from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('id','product')
    ordering = ('product',)

admin.site.register(Product,ProductAdmin)