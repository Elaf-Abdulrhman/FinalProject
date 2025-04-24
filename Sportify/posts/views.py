from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from .models import Post
from .forms import PostForm


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # <-- include request.FILES
        if form.is_valid():
            form.save()
            return redirect('posts:all_posts')
    else:
        form = PostForm()
    return render(request, 'posts/add_post.html', {'form': form})


def all_posts(request):
    posts_list = Post.objects.all().order_by('-created_at')
    page = int(request.GET.get('page', 1))  # Get the current page number
    per_page = 6  # Number of posts per page
    start = (page - 1) * per_page
    end = page * per_page
    posts = posts_list[start:end]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        posts_data = [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author,
                'photo_url': post.photo.url if post.photo else None,
                'created_at': post.created_at.strftime('%B %d, %Y'),
            }
            for post in posts
        ]
        return JsonResponse({'posts': posts_data})

    return render(request, 'posts/all_posts.html', {'posts': posts_list[:per_page]})


def post_details(request, post_id):
    # Retrieve the post by its ID or return a 404 if not found
    post = get_object_or_404(Post, pk=post_id)
    
    context = {
        'post': post,
    }

    return render(request, 'posts/post_details.html', context)

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:all_posts')
    return render(request, 'posts/delete_post.html', {'post': post})

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # <-- include request.FILES
        if form.is_valid():
            form.save()
            return redirect('posts:post_details', post_id=post.pk)  # Redirect to the updated post details
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})