from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from account.models import Club
from django.db.models import Q

# Create your views here.
def all_clubs(request):
    clubs = Club.objects.all()  

    search_query = request.GET.get("q", "")
    if search_query:
        clubs = clubs.filter(
            Q(clubName__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    return render(request, 'clubs/all_clubs.html', {"clubs": clubs})