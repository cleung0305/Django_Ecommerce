from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.template import RequestContext, Context
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
        return render(request, self.template_name)

def checkout(request):
    return render(request, 'checkout.html')