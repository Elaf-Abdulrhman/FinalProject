from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q, Max, Count
from django.contrib import messages

@login_required
def chat_page_view(request, username=None):
    if request.user.is_superuser:
        return redirect('admins:dashboard')

    search_query = request.GET.get('q', '')
    selected_user = None
    chat_messages = []
    unread_counts = {}

    if search_query:
        users = User.objects.filter(
            username__icontains=search_query,
            is_superuser=False
        ).exclude(id=request.user.id)
    else:
        # Get users with whom the current user has chatted
        sent_times = Message.objects.filter(sender=request.user).values('recipient').annotate(last=Max('timestamp'))
        received_times = Message.objects.filter(recipient=request.user).values('sender').annotate(last=Max('timestamp'))

        last_message_map = {}

        for entry in sent_times:
            last_message_map[entry['recipient']] = entry['last']
        for entry in received_times:
            existing = last_message_map.get(entry['sender'])
            if not existing or entry['last'] > existing:
                last_message_map[entry['sender']] = entry['last']

        # Get unread message counts (clean and correct)
        unread_counts_qs = (
            Message.objects
            .filter(recipient=request.user, is_read=False)
            .values('sender')
            .annotate(count=Count('id'))
        )
        unread_counts = {entry['sender']: entry['count'] for entry in unread_counts_qs}

        # Build user queryset and sort by last message timestamp
        user_ids = last_message_map.keys()
        users_qs = User.objects.filter(id__in=user_ids, is_superuser=False).exclude(id=request.user.id)
        users = sorted(users_qs, key=lambda u: last_message_map[u.id], reverse=True)

    if username:
        try:
            selected_user = User.objects.get(username=username)
            if selected_user.is_superuser or selected_user.id == request.user.id:
                selected_user = None
                messages.error(request, "You cannot chat with this user.")
            else:
                # Mark messages as read
                Message.objects.filter(
                    sender=selected_user,
                    recipient=request.user,
                    is_read=False
                ).update(is_read=True)

                # Load chat history
                chat_messages = Message.objects.filter(
                    Q(sender=request.user, recipient=selected_user) |
                    Q(sender=selected_user, recipient=request.user)
                ).order_by('timestamp')
        except User.DoesNotExist:
            print("!!! USER NOT FOUND !!!")
            messages.error(request, f"No user found with username '{username}'.")

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
        'unread_counts': unread_counts,
    })
