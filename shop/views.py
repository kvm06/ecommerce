from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse(request, "shop/home.html")

def about(request):
    return render(request, "shop/about.html")
