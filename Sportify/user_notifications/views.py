from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def inbox(request):
    notifications = Notification.objects.unread().filter(recipient=request.user)
    notifications.mark_all_as_read()  # Mark notifications as read
    return render(request, 'user_notifications/inbox.html', {'notifications': notifications})
