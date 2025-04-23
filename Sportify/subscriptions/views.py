from django.shortcuts import render

def plus_plan(request):
    return render(request, 'subscriptions/plus_plan.html')

def payment(request):
    if request.method == 'POST':
        # Handle the payment processing here
        # For example, you can use a payment gateway API
        # to process the payment and create a subscription
        pass

    return render(request, 'subscriptions/payment.html')
