from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from django_resized import ResizedImageField
from datetime import datetime
import random
import string

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('I', 'info')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

STATES_CHOICES = (
    ("Alabama","Alabama"),("Alaska","Alaska"),("Arizona","Arizona"),("Arkansas","Arkansas"),("California","California"),("Colorado","Colorado"),("Connecticut","Connecticut"),("Delaware","Delaware"),("Florida","Florida"),("Georgia","Georgia"),("Hawaii","Hawaii"),("Idaho","Idaho"),("Illinois","Illinois"),("Indiana","Indiana"),("Iowa","Iowa"),("Kansas","Kansas"),("Kentucky","Kentucky"),("Louisiana","Louisiana"),("Maine","Maine"),("Maryland","Maryland"),("Massachusetts","Massachusetts"),("Michigan","Michigan"),("Minnesota","Minnesota"),("Mississippi","Mississippi"),("Missouri","Missouri"),("Montana","Montana"),("Nebraska","Nebraska"),("Nevada","Nevada"),("New Hampshire","New Hampshire"),("New Jersey","New Jersey"),("New Mexico","New Mexico"),("New York","New York"),("North Carolina","North Carolina"),("North Dakota","North Dakota"),("Ohio","Ohio"),("Oklahoma","Oklahoma"),("Oregon","Oregon"),("Pennsylvania","Pennsylvania"),("Rhode Island","Rhode Island"),("South Carolina","South Carolina"),("South Dakota","South Dakota"),("Tennessee","Tennessee"),("Texas","Texas"),("Utah","Utah"),("Vermont","Vermont"),("Virginia","Virginia"),("Washington","Washington"),("West Virginia","West Virginia"),("Wisconsin","Wisconsin"),("Wyoming","Wyoming")
    )

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    stripe_customer_id = models.CharField(max_length=50, default="00000", blank=True, null=True)
    one_click_purchasing = models.BooleanField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, default="default.jpg")

    def __str__(self):
        return f"Profile of user: {self.user.username}"

class Item(models.Model):
    """Single Item object. contains the item's title, price, category, etc...
    """
    title = models.CharField(max_length = 100)
    price = models.FloatField(default=0)
    discount_price = models.FloatField(blank=True, null = True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length = 2)
    label = models.CharField(choices=LABEL_CHOICES, max_length = 1)
    slug = models.SlugField(blank = True, null = True, unique = True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    new = models.BooleanField(default=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        num = 1
        slug = slugify(self.title)
        unique_slug = '{}-{}'.format(slug, num)
        while Item.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        }) 

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        }) 

    

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_total_item_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('Address', related_name="billing_address", on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey('Address', related_name="shipping_address", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=10, null=True, blank=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)



    def __str__(self):
        return self.user.username

    def total_order_price(self):
        total = 0
        for item in self.items.all():
            total+=item.get_final_total_item_price()
        return total

    def discount_amount(self):
        if self.coupon:
            amount = self.total_order_price() * (self.coupon.amount/100)
            return amount
        return 0
    
    def total_order_price_with_discount(self):
        return self.total_order_price() - self.discount_amount()

    def final_price(self):
        if self.coupon:
            return self.total_order_price_with_discount()
        return self.total_order_price()

    def generate_random_string(self):
        size = 10
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choices(chars, k=size))

    def generate_order_number(self):
        new_num = self.generate_random_string()
        while Order.objects.filter(order_number=new_num).exists():
            new_num = self.generate_random_string()
        return new_num

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="address")
    email = models.EmailField(max_length=200, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    state = models.CharField(max_length=100)
    zip_address = models.CharField(max_length=100)
    address_type = models.CharField(choices=ADDRESS_CHOICES, max_length=1)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.state}"

    def is_valid(self):
        if self.street_address == "":
            return False
        return True

    class Meta:
        verbose_name_plural = "Addresses"

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=10)
    amount = models.FloatField(default=10)
    description = models.CharField(max_length=100, default='New Promo!')

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_userprofile")
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
        userprofile.save()
