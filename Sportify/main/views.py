from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Avg
from account.models import User, Athlete,Club

def main_page_view(request):
    athletes=Athlete.objects.all()
    clubs = Club.objects.all() 
    
    return render(request, 'main/main_page.html',{"athletes":athletes, "clubs": clubs})





def about_page_view(request):
    return render(request, 'main/about_us.html')


def mode_view(request:HttpRequest, mode):

    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light")
    elif mode == "dark":
        response.set_cookie("mode", "dark")


    return response