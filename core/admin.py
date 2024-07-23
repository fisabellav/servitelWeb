from django.contrib import admin
from .models import Order, OrderDetail



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('get_order_id', 'get_order_user', 'product', 'quantity')

    def get_order_id(self, obj):
        return obj.order.id
    get_order_id.short_description = 'Pedido'

    def get_order_user(self, obj):
        return obj.order.user
    get_order_user.short_description = 'Cliente'



admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)



