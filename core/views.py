from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.template import RequestContext, Context
from django.utils import timezone
from .models import *

# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return render(request, self.template_name, context)

class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        return render(request, self.template_name, context)

class CheckoutView(ListView):
    model = Order
    template_name = "checkout.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
    order_queryset = Order.objects.filter(user=request.user, ordered=False)
    if order_queryset.exists():
        order = order_queryset[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product", slug=slug)