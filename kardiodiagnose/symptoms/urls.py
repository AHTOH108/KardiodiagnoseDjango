from django.urls import path
from symptoms.views import *

urlpatterns = [
    path('', index),
]