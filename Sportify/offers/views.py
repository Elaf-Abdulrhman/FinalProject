from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required


from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from .forms import OfferForm
from .models import Offer

def add_offer(request):
    if not hasattr(request.user, 'club'):
        return HttpResponseForbidden("Only clubs can add offers.")

    club = request.user.club

    if not club.is_premium:
        one_week_ago = timezone.now() - timedelta(days=7)
        offers_last_week = Offer.objects.filter(user=request.user, created_at__gte=one_week_ago).count()

        if offers_last_week >= 3:
            messages.error(request, "You can only post 3 offers per week. Upgrade your plan to post unlimited offers!","alert-danger")
            return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.save()
            messages.success(request, "Your offer has been successfully posted.", "alert-success")
            return redirect('offers:all_offers')
    else:
        form = OfferForm()

    return render(request, 'offers/add_offer.html', {'form': form})


def all_offers(request):
    offers_list = Offer.objects.all().order_by('-created_at')
    page = int(request.GET.get('page', 1))
    per_page = 6
    start = (page - 1) * per_page
    end = page * per_page
    offers = offers_list[start:end]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        offers_data = [
            {
                'id': offer.id,
                'title': offer.title,
                'content': offer.content,
                'author': offer.user.username,
                'photo_url': offer.photo.url if offer.photo else None,
                'created_at': offer.created_at.strftime('%B %d, %Y'),
            }
            for offer in offers
        ]
        return JsonResponse({'offers': offers_data})

    return render(request, 'offers/all_offers.html', {'offers': offers_list[:per_page]})

def offer_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offers/offer_details.html', {'offer': offer})

def delete_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        offer.delete()
        return redirect('offers:all_offers')
    return render(request, 'offers/delete_offer.html', {'offer': offer})

def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('offers:offer_details', offer_id=offer.pk)
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form, 'offer': offer})



@login_required
def my_offers(request):
    if not hasattr(request.user, 'club'):
        return redirect('offers:all_offers')

    user_offers = Offer.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'offers/my_offers.html', {'offers': user_offers})
