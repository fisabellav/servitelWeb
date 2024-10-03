from django.contrib import admin
from .models import Payment, Client
from core.models import Order

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_order_id', 'get_order_user', 'amount', 'payment_date')

    def get_order_id(self, obj):
        return obj.order.id
    get_order_id.short_description = 'Pedido'

    def get_order_user(self, obj):
        return obj.order.user
    get_order_user.short_description = 'Cliente'


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'adress', 'phone')

admin.site.register(Client, ClientAdmin)

admin.site.register(Payment, PaymentAdmin)