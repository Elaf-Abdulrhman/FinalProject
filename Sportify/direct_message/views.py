# messages/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message

# messages/views.py
@login_required
def inbox_view(request):
    users = User.objects.exclude(id=request.user.id)

    # Prepare the unread counts for each user
    unread_counts = {}
    for user in users:
        unread_count = Message.objects.filter(
            recipient=user, 
            is_read=False
        ).exclude(sender=request.user).count()
        unread_counts[user.id] = unread_count  # Store unread count by user ID

    # Pass unread_counts dictionary to the template
    return render(request, 'direct_message/inbox.html', {
        'users': users,
        'unread_counts': unread_counts
    })

@login_required
def direct_chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    # Mark messages as read
    unread_messages = Message.objects.filter(
        recipient=request.user,
        sender=other_user,
        is_read=False
    )
    unread_messages.update(is_read=True)  # Update all unread messages to 'read'

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=other_user, content=content)
            return redirect('direct_message:direct_chat_view', username=username)

    # Fetch the messages between the two users
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    )

    return render(request, 'direct_message/chat.html', {
        'messages': messages,
        'other_user': other_user
    })

