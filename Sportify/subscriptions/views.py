# subscriptions/views.py

import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .models import Payment
from account.models import Club

def payment_success(request):
    payment_id = request.GET.get('id')

    if not payment_id:
        return render(request, 'subscriptions/payment_failed.html', {'error': 'Missing payment ID'})

    url = f"https://api.moyasar.com/v1/payments/{payment_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {settings.MOYASAR_SECRET_KEY}:'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            payment_data = response.json()

            if payment_data.get('status') == 'paid':
                created_at_raw = payment_data.get('created_at')
                if created_at_raw:
                    created_at = parse_datetime(created_at_raw)
                else:
                    created_at = datetime.now()

                if request.user.is_authenticated:
                    Payment.objects.create(
                        user=request.user,
                        payment_id=payment_data['id'],
                        amount=payment_data['amount'],
                        status=payment_data['status'],
                        created_at=created_at,
                    )

                    if hasattr(request.user, 'club'):
                        club = request.user.club
                        club.is_premium = True
                        club.save()
                        messages.success(request, "Congratulations! Your club has been upgraded to Plus Plan!")

                return render(request, 'subscriptions/payment_success.html', {'payment': payment_data})

            else:
                return render(request, 'subscriptions/payment_failed.html', {'error': 'Payment not completed'})
        else:
            error_message = response.json().get('message', 'Failed to verify payment')
            return render(request, 'subscriptions/payment_failed.html', {'error': error_message})

    except Exception as e:
        return render(request, 'subscriptions/payment_failed.html', {'error': str(e)})

def payment(request):
    return render(request, 'subscriptions/payment.html', {
        'moyasar_publishable_key': settings.MOYASAR_PUBLISHABLE_KEY,
    })


def plus_plan(request):
    return render(request, 'subscriptions/plus_plan.html')
