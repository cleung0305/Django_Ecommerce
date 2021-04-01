from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.template import RequestContext, Context
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import CheckoutForm

# Create your views here.

class HomeView(ListView):
    model = Item
    paginate_by = 20
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return render(request, self.template_name, context)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object":order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect("/")

class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        return render(request, self.template_name, context)

class CheckoutView(View):
    model = Order
    template_name = "checkout.html"
    context = {}
    def get(self, *args, **kwargs):
        #forms
        form = CheckoutForm()
        self.context = {
            'form':form
        }
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                states = form.cleaned_data.get('states')
                zip_address = form.cleaned_data.get('zip_address')
                
                
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    email = email,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    city=city,
                    country=country,
                    states=states,
                    zip_address=zip_address
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('core:payment', payment_option = payment_option)
            messages.warning(self.request, 'Failed Checkout')
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect("core:order-summary")

class PaymentView(View):
    template_name = 'payment.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


@login_required
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
            messages.info(request, "Your cart was updated.")
            # return redirect("core:product", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            # return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("core:product", slug=slug)

@login_required
def add_single_item_to_cart(request, slug):
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
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:order-summary")
    else:
        messages.info(request, "You do not have any order.")
        return redirect("core:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.user.is_anonymous:
        messages.info(request,"You are not logged in.")
        return redirect("core:product", slug=slug)
    else:
        order_queryset = Order.objects.filter(user=request.user, ordered=False)
        if order_queryset.exists():
            order = order_queryset[0]
            #check if order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart.")
                return redirect("core:order-summary")
            else: 
                #add a message saying the user does not have any order.
                messages.info(request, "This item was not in your cart.")
                return redirect("core:order-summary")
        else:
            #add a message saying the user does not have any order.
            messages.info(request, "You do not have any ordeer.")
            return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.user.is_anonymous:
        messages.info(request,"You are not logged in.")
        return redirect("core:order-summary")
    else:
        order_queryset = Order.objects.filter(user=request.user, ordered=False)
        if order_queryset.exists():
            order = order_queryset[0]
            #check if order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                if(order_item.quantity > 1):
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, "This item quantity was updated.")
                else:
                    order.items.remove(order_item)
                    messages.info(request, "This item was removed from your cart.")
                return redirect("core:order-summary")
            else: 
                #add a message saying the user does not have any order.
                messages.info(request, "This item was not in your cart.")
                return redirect("core:order-summary")
        else:
            #add a message saying the user does not have any order.
            messages.info(request, "You do not have any ordeer.")
            return redirect("core:order-summary")