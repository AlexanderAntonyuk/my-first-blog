from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm, UserForm, LoginForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def post_list(request):
    superuser = User.objects.all().filter(is_superuser=True)
    posts = Post.objects.filter(author_id = superuser[0]).filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})         

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username, email, password)
            user.date_joined = timezone.now()
            return redirect('sigh_in')
    else:
        form = UserForm()
    return render(request, 'blog/registration.html', {'form': form})

def sigh_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        form = LoginForm(request.POST)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

def dashboard(request):
    posts = Post.objects.filter(author_id = request.user).filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/dashboard.html', {'page_obj': page_obj})

def logout_user(request):
    logout(request)
    return redirect('sigh_in')