from django.contrib import admin
from .models import Item, OrderItem, Order, Payment, Coupon, Address, Refund, UserProfile
# Register your models here.


class OrderAdmin(admin.ModelAdmin):

    # custon action : make refund accepted
    def make_refund_accepted(modeladmin, request, queryset):
        queryset.update(refund_requested=False, refund_granted=True)

    make_refund_accepted.short_description = "Update orders to refund granted."

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
                    'shipping_address',
                    'payment',
                    'coupon']
    list_display_links = ['user',
                        'billing_address',
                        'shipping_address',
                        'payment',
                        'coupon']
    list_filter = [ 'ordered', 
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted']
    search_fields = ['user__username',
                    'order_number']

    actions = [make_refund_accepted]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_detail', 'ordered']

    def item_detail(self, obj):
        return '{quantity} of {title}'.format(quantity = obj.quantity, title = obj.item.title)

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'email',
        'street_address',
        'apartment_address',
        'city',
        'country',
        'state',
        'zip_address',
        'address_type',
        'default'
    ]

    list_filter = ['address_type', 'default', 'country']

    search_fields = ['user', 'email', 'zip_address']

admin.site.register(Item)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)

