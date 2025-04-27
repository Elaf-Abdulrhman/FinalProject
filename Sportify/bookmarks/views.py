from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Bookmark
from posts.models import Post
from .models import Bookmark

@login_required
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

    if not created:
        # If the bookmark already exists, remove it
        bookmark.delete()

    return redirect('posts:post_details', post_id=post.id)

@login_required
def all_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post')
    return render(request, 'bookmarks/all_bookmarks.html', {'bookmarks': bookmarks})