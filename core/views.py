from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.template import RequestContext, Context
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import CheckoutForm, CouponForm, RefundForm

import time
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

class HomeView(ListView):
    model = Item
    paginate_by = 20
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object":order,
                'couponform':CouponForm(),
                'DISPLAY_COUPON_FORM': True,
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any order.")
            return redirect("/")

class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        return render(request, self.template_name, context)

class CheckoutView(View):
    template_name = "checkout.html"
    context = {}
    def get(self, *args, **kwargs):
        #forms
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            self.context = {
                'form':form,
                'couponform':CouponForm(),
                'order':order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, self.template_name, self.context)
        except:
            messages.error(self.request, 'You do not have any order')
            return redirect('core:checkout')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                data = form.cleaned_data
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')

                # payment_option = form.cleaned_data.get('payment_option')
                payment_option = data['payment_option']
                billing_address = BillingAddress(
                    user=self.request.user,
                    email = data['email'],
                    street_address=data['street_address'],
                    apartment_address=data['apartment_address'],
                    city=data['city'],
                    country=data['country'],
                    states=data['states'],
                    zip_address=data['zip_address']
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                
                print(form.cleaned_data)
                if payment_option == 'C':
                    return redirect('core:payment', payment_option = 'Card')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option = 'Paypal')
                else:
                    messages.warning(self.request, 'Invalid payment option selected.')
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")

class PaymentView(View):
    template_name = 'payment.html'

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order':order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, self.template_name, context)
        else:
            messages.error(self.request, "You have not added a billing address.")
            return redirect('core:checkout')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.final_price() * 100) #cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="My First Test Charge (created for API docs)",
            )
             #make the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.final_price()
            payment.save()

            #set order item to be ordered
            order_items = order.items.all()
            order_items.update(ordered=True, ordered_date=timezone.now())
            for item in order_items:
                item.save()

            #assign the payment to order
            order.ordered = True
            order.ordered_date = timezone.now()
            order.payment = payment
            order.order_number = order.generate_order_number()
            order.save()

            messages.success(self.request, "Your order has been placed. Thank you!")
            return redirect("/")

        except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
            messages.warning(self.request, f"Card Error. {e.user_message}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, f"Rate Limit Error. {e.user_message}")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, f"Invalid Parameters. {e.user_message}")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, f"Not Authenticated. {e.user_message}")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, f"API Connection Error. {e.user_message}")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, f"Payment Failed. Your were not charged. Please try again later. {e.user_message}")
            return redirect("/")
        except Exception as e:
            # send email to ourselves
            messages.warning(self.request, f"Something went wrong. {e.user_message}")
            return redirect("/")



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
        # check if order item is in the order
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
        order = Order.objects.create(user=request.user)
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
        messages.warning(request, "You do not have any order.")
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

                order_item.quantity = 1
                order_item.save()
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
            messages.info(request, "You do not have any order.")
            return redirect("core:order-summary")


def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                code = form.cleaned_data.get('code')
                order.coupon = get_coupon(self.request, code)
                order.save()

                messages.success(self.request, "Coupon applied")
                return redirect("core:checkout")

            except ValueError:
                messages.error(self.request, "Coupon invalid")
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have any order")
                return redirect("core:home")
    

class RequestRefundView(View):
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            order_number = form.cleaned_data.get('order_number')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            try:
                order = Order.objects.get(order_number=order_number)
                order.refund_requested = True
                order.save()
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.emal = email
                refund.save()
            except ObjectDoesNotExist:
                messages.warning(self.request, "Order not found. Please make sure this is the right order number.")
                return redirect("core:request-refund")
            finally:
                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")