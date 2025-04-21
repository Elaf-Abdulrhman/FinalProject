from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import Avg

def main_page_view(request):
    return render(request, 'main/main_page.html')





def about_page_view(request):
    return render(request, 'main/about_us.html')