from django.urls import path
from .views import *

app_name = 'theme'

urlpatterns = [
    path('inbox/', InboxView.as_view(), name='inbox'),
]