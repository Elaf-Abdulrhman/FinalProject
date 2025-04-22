from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Offer
from .forms import OfferForm

def add_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)  # <-- include request.FILES
        if form.is_valid():
            form.save()
            return redirect('offers:all_offers')
    else:
        form = OfferForm()
    return render(request, 'offers/add_offer.html', {'form': form})

def all_offers(request):
    offers_list = Offer.objects.all().order_by('-created_at')
    page = int(request.GET.get('page', 1))  # Get the current page number
    per_page = 6  # Number of offers per page
    start = (page - 1) * per_page
    end = page * per_page
    offers = offers_list[start:end]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        offers_data = [
            {
                'id': offer.id,
                'title': offer.title,
                'content': offer.content,
                'author': offer.author,
                'photo_url': offer.photo.url if offer.photo else None,
                'created_at': offer.created_at.strftime('%B %d, %Y'),
            }
            for offer in offers
        ]
        return JsonResponse({'offers': offers_data})

    return render(request, 'offers/all_offers.html', {'offers': offers_list[:per_page]})

def offer_details(request, offer_id):
    # Retrieve the offer by its ID or return a 404 if not found
    offer = get_object_or_404(Offer, pk=offer_id)
    
    context = {
        'offer': offer,
    }

    return render(request, 'offers/offer_details.html', context)

def delete_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        offer.delete()
        return redirect('offers:all_offers')
    return render(request, 'offers/delete_offer.html', {'offer': offer})

def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)  # <-- include request.FILES
        if form.is_valid():
            form.save()
            return redirect('offers:offer_details', offer_id=offer.pk)  # Redirect to the updated offer details
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/edit_offer.html', {'form': form, 'offer': offer})
