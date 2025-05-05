# messages/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message

@login_required
def chat_page_view(request, username=None):
    users = User.objects.exclude(id=request.user.id)
    selected_user = None
    chat_messages = []

    if username:
        selected_user = get_object_or_404(User, username=username)

        # ✅ Mark unread messages as read (just run it, don't assign it)
        Message.objects.filter(
            sender=selected_user,
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        # ✅ Get conversation messages
        chat_messages = Message.objects.filter(
            sender__in=[request.user, selected_user],
            recipient__in=[request.user, selected_user]
        ).order_by('timestamp')

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
    })
