from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/<str:category>/', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('add-coupon/', AddCouponView.as_view(), name="add-coupon"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('remove-single_item_from-cart/<slug>/', remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('add_single_item_to_cart/<slug>/', add_single_item_to_cart, name="add-single-item-to-cart"),
    path('request-refund/', RequestRefundView.as_view(), name="request-refund"),
]