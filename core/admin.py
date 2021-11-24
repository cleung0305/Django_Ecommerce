from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon, BillingAddress, Refund
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 
                    'order_number',
                    'ordered', 
                    'start_date', 
                    'final_price',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'payment',
                    'coupon']
    list_display_links = ['user',
                        'billing_address',
                        'payment',
                        'coupon']
    list_filter = [ 'ordered', 
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted']
    search_fields = ['user__username',
                    'order_number']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_detail', 'ordered']

    def item_detail(self, obj):
        return '{quantity} of {title}'.format(quantity = obj.quantity, title = obj.item.title)


admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
