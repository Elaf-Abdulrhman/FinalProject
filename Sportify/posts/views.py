from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    # Get all posts and apply pagination
    posts_list = Post.objects.all().order_by('-created_at')  # Order posts by creation date (latest first)
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page

    page_number = request.GET.get('page')  # Get current page from query params
    page_obj = paginator.get_page(page_number)  # Get page object

    context = {
        'posts': page_obj,
    }

    return render(request, 'posts/all_posts.html', context)

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
