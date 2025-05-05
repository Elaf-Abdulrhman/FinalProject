# messages/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max

@login_required
def chat_page_view(request, username=None):
    search_query = request.GET.get('q', '')

    # ✅ Users with chat history (either sent or received)
    chat_partners = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).values('sender', 'recipient')

    user_ids = set()
    for entry in chat_partners:
        user_ids.update([entry['sender'], entry['recipient']])
    user_ids.discard(request.user.id)

    users_with_chat = User.objects.filter(id__in=user_ids)

    # ✅ Annotate with last message time & order by recent
    users = users_with_chat.annotate(
        last_message=Max('sent_messages__timestamp')  # assumes related_name
    ).order_by('-last_message')

    # ✅ If searching
    if search_query:
        users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)

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

        # Get conversation
        chat_messages = Message.objects.filter(
            sender__in=[request.user, selected_user],
            recipient__in=[request.user, selected_user]
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
        'selected_user': selected_user,
        'chat_messages': chat_messages,
        'search_query': search_query,
    })
