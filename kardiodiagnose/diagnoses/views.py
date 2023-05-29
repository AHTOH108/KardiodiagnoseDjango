from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'diagnoses/index.html')

def about_view(request):
    return render(request, 'diagnoses/about.html', {'title': 'Это значение передали из view'})