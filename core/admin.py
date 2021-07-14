from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon, BillingAddress
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'final_price']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_detail', 'ordered']

    def item_detail(self, obj):
        return '{quantity} of {title}'.format(quantity = obj.quantity, title = obj.item.title)


admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
