from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('posts:all_posts')
    else:
        form = PostForm()
    return render(request, 'posts/add_post.html', {'form': form})



def all_posts(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 6)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'posts/all_posts.html', {'posts': posts})

def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_details.html', {'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
            messages.success(request, "Post deleted.")
            return redirect('posts:all_posts')
    else:
        messages.error(request, "You are not authorized to delete this post.")
    return render(request, 'posts/delete_post.html', {'post': post})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('posts:post_details', post_id=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "you updated you post seccessfully!.")
            return redirect('posts:post_details', post_id=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})
