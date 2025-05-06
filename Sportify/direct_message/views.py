# messages/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max

from django.contrib.auth.models import User
from django.db.models import Q, Max
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_page_view(request, username=None):
    search_query = request.GET.get('q', '')

    # ✅ Search for all users except the logged-in user
    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
    else:
        # If no search query, fetch all users except the logged-in user
        users = User.objects.exclude(id=request.user.id)

    # Prepare to display the chat if a user is selected
    selected_user = None
    chat_messages = []

    if username:
        selected_user = get_object_or_404(User, username=username)

        # Mark messages as read
        Message.objects.filter(
            sender=selected_user,
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        # Get conversation between the logged-in user and the selected user
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
