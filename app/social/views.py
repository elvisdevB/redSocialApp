from multiprocessing import current_process
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Posr, Relationship
from django.contrib import messages
from .forms import PostForm, UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def feed(request):
    post = Posr.objects.all()

    context = {
        'post':post
    }
    return render(request,'social/feed.html', context)

def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        post = user.post.all()
    else:
        post = current_user.post.all()
        user = current_user
    return render(request, 'social/profile.html', {'user':user, 'post':post})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado correctamente')
            return redirect('feed')
    else:
        form = UserRegisterForm()

    context = {
        'form':form
    }   
    return render(request, 'social/register.html', context)

@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, "Se ha registrado correctamente")
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social/post.html', {'form':form})


def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Sigues a {username}')
    return redirect('feed')

def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect('feed')
