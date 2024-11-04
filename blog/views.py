from django.forms import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Post
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import render
from datetime import timedelta

def home(request):
    latest_posts = Post.objects.filter(approved=True).order_by('-created_date')[:5]
    most_viewed_posts = Post.objects.filter(approved=True).order_by('-views')[:5]
    one_week_ago = timezone.now() - timedelta(days=7)
    weekly_popular_posts = Post.objects.filter(approved=True, created_date__gte=one_week_ago).order_by('-views')[:5]
    one_month_ago = timezone.now() - timedelta(days=30)
    monthly_popular_posts = Post.objects.filter(approved=True, created_date__gte=one_month_ago).order_by('-views')[:5]

    context = {
        'latest_posts': latest_posts,
        'most_viewed_posts': most_viewed_posts,
        'weekly_popular_posts': weekly_popular_posts,
        'monthly_popular_posts': monthly_popular_posts,
    }

    return render(request, 'blog/home.html', context)



@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})


def post_list(request):
    posts = Post.objects.filter(approved=True)  # Only show approved posts

    # Check if a search query is present
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'blog/post_list.html', {'posts': posts, 'query': query})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('register')  # Redirect back to the registration page

        # If username is unique, create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'blog/register.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1
    post.save()
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.text = request.POST.get('text')
        comment.save()
        return redirect('post_detail', post_id=comment.post.id)
    return render(request, 'blog/edit_comment.html', {'comment': comment})



