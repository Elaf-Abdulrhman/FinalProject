# subscriptions/views.py

import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .models import Payment  # Assuming you have a Payment model


def payment_success(request):
    payment_id = request.GET.get('id')
    # Check if payment ID is missing in the request
    if not payment_id:
        return render(request, 'subscriptions/payment_failed.html', {'error': 'Missing payment ID'})

    # Moyasar API endpoint
    url = f"https://api.moyasar.com/v1/payments/{payment_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {settings.MOYASAR_SECRET_KEY}:'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            payment_data = response.json()
            print(f"Payment Data: {payment_data}")  # Debugging

            # Check if the payment status is 'paid'
            if payment_data.get('status') == 'paid':
                # Save payment information to the database
                Payment.objects.create(
                    payment_id=payment_data['id'],
                    amount=payment_data['amount'],
                    status=payment_data['status'],
                )
                return render(request, 'subscriptions/payment_success.html', {'payment': payment_data})
            else:
                # Payment status is not 'paid'
                return render(request, 'subscriptions/payment_failed.html', {'error': 'Payment not completed'})
        else:
            # Failed to fetch payment details from Moyasar API
            error_message = response.json().get('message', 'Failed to verify payment')
            return render(request, 'subscriptions/payment_failed.html', {'error': error_message})
    except Exception as e:
        # Handle exceptions
        return render(request, 'subscriptions/payment_failed.html', {'error': str(e)})


def payment(request):
    return render(request, 'subscriptions/payment.html', {
        'moyasar_publishable_key': settings.MOYASAR_PUBLISHABLE_KEY,
    })


def plus_plan(request):
    return render(request, 'subscriptions/plus_plan.html')
