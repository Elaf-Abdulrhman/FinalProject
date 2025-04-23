import stripe
from django.conf import settings
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

def plus_plan(request):
    return render(request, 'subscriptions/plus_plan.html')

def payment(request):
    if request.method == 'POST':
        try:
            # Create a payment intent
            intent = stripe.PaymentIntent.create(
                amount=111,  # Amount in hallalah (e.g., $9.99)
                currency='sar',
                payment_method=request.POST['payment_method_id'],
                confirm=True,
            )
            return render(request, 'subscriptions/payment_success.html', {'intent': intent})
        except stripe.error.CardError as e:
            return render(request, 'subscriptions/payment_failed.html', {'error': str(e)})
    else:
        return render(request, 'subscriptions/payment.html', {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        })
