from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homepage(request):
    return render(request, 'bookepedia/homepage.html')

def add_a_book(request):
    return render(request, 'bookepedia/add_a_book.html')
