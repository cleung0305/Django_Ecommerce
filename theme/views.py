from django.views.generic import View, DetailView, ListView
from django.shortcuts import render, redirect, get_object_or_404

class InboxView(View):
    template_name = 'inbox.html'

    def get(self, request):
        return render(request, self.template_name, {})