from django.shortcuts import render
from account.models import User, Athlete
from django.db.models import Q
# Create your views here.
def all_athletes(request):
    athletes=Athlete.objects.all()
    search_query = request.GET.get("q", "")
    if search_query:
        athletes = athletes.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )

    return render(request, 'athlete/all_athletes.html',{"athletes":athletes})



