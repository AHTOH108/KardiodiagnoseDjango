from django.urls import path
from diagnoses.views import *

urlpatterns = [
    path('', index),
    path('about/', about_view),
    path('logout/', logout_user, name='logout'),
]