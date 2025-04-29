from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import Avg
from account.models import User, Athlete,Club

def main_page_view(request):
    athletes=Athlete.objects.all()
    clubs = Club.objects.all() 
    
    return render(request, 'main/main_page.html',{"athletes":athletes, "clubs": clubs})





def about_page_view(request):
    return render(request, 'main/about_us.html')