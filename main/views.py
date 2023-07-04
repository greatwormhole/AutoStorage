from django.shortcuts import render
from django.views.generic import ListView

def test(request):
    return render(request, 'main/main.html')
