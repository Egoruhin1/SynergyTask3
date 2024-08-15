from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Post, Profile, Comment
from .forms import UserRegisterForm, PostForm, CommentForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('blog-home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post-detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post-detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('post-detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog-home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(public=True).order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments})

@login_required
def subscribe_user(request, username):
    user_to_subscribe = get_object_or_404(User, username=username)
    try:
        profile = request.user.profile
        user_profile = user_to_subscribe.profile
    except Profile.DoesNotExist:
        messages.error(request, 'Profile does not exist for the user.')
        return redirect('user-posts', username=username)

    if profile.subscriptions.filter(pk=user_profile.pk).exists():
        profile.subscriptions.remove(user_profile)
        messages.success(request, f'You have unsubscribed from {username}.')
    else:
        profile.subscriptions.add(user_profile)
        messages.success(request, f'You have subscribed to {username}.')
    return redirect('user-posts', username=username)

@login_required
def subscription_posts(request):
    try:
        profile = request.user.profile
        profiles = profile.subscriptions.all()
        posts = Post.objects.filter(author__profile__in=profiles).order_by('-created_at')
    except Profile.DoesNotExist:
        messages.error(request, 'Profile does not exist for the user.')
        return redirect('blog-home')
    return render(request, 'blog/subscription_posts.html', {'posts': posts})

@login_required
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {'posts': posts, 'user': user})

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'blog/profile.html', {'user': user})


