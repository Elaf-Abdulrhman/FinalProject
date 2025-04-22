from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse

# Create your views here.

def sign_up_as_view(request:HttpRequest):\
    return render(request,"account/sign_up_as.html")