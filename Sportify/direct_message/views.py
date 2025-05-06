# messages/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max

@login_required
def chat_page_view(request, username=None):
    search_query = request.GET.get('q', '')
    selected_user = None
    chat_messages = []

    if search_query:
        # Show matching users except the current user
        users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    else:
        # Only users the current user has had conversations with
        users = User.objects.filter(
            Q(sent_messages__recipient=request.user) |
            Q(received_messages__sender=request.user)
        ).exclude(id=request.user.id).distinct()

    if username:
        selected_user = get_object_or_404(User, username=username)

        # Mark messages as read
        Message.objects.filter(
            sender=selected_user,
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        # Get the conversation
        chat_messages = Message.objects.filter(
            Q(sender=request.user, recipient=selected_user) |
            Q(sender=selected_user, recipient=request.user)
        ).order_by('timestamp')

    # Handle sending a message
    if request.method == 'POST' and selected_user:
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=selected_user,
                content=content
            )
            return redirect('direct_message:chat_page', username=selected_user.username)

    return render(request, 'direct_message/combined_chat.html', {
        'users': users,
        'selected_user': selected_user,
        'chat_messages': chat_messages,
        'search_query': search_query,
    })
