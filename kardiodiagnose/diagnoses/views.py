from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

from diagnoses.models import Diagnose

def index(request):
    list = Diagnose.objects.all()
    list = [i.name for i in list]
    print(request.user.is_auth)
    return render(request, 'diagnoses/index.html', {'list_object': list})

def about_view(request):
    return render(request, 'diagnoses/about.html', {'title': 'Это значение передали из view'})

def logout_user(request):
    logout(request)
    return redirect('')