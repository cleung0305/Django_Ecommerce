from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
]