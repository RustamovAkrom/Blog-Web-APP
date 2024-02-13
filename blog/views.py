from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse

from django.views.generic import (DeleteView, 
                                  UpdateView, 
                                  CreateView, 
                                  DetailView)

from django.views.generic import TemplateView
from django.views.generic.list import ListView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

from django.core.paginator import Paginator

from .forms import *
from .models import *

import datetime

#User authentificate class
#====================================================================

class RegisterPageView(View):
    def get(self, request):
        return render(request, "blog/register.html", { "form":RegisterForm() })

    def post(self, request):

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "User succesfully registered")
            return redirect("login")
        else:
            messages.warning(request, 'Error registered!')
            return render(request, "blog/register.html", { "form":form })


class LoginPageView(View):
    def get(self, request):
        return render(request, "blog/login.html", { "form":LoginForm() })
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as { username }")
                return redirect('home')
            
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')

        return render(request, "blog/login.html", { "form":form })


class LogoutView(View):
    def get(self, request):
        return render(request, "blog/logout.html")
    
    def post(self, request):
        logout(request)
        return redirect('home')

#Blog Pages
#===================================================================
    
class HomePageView(View):
    def get(self, request):
        
        if request.user.is_authenticated: 
            posts = Post.objects.exclude(author=request.user)

        else: 
            posts = Post.objects.all()
        posts = posts.filter(is_active=True).order_by('id')

        page = request.GET.get('page', 1)
        size  = request.GET.get('size', 4)
        paginator = Paginator(posts.order_by('id'), size)
        page_obj = paginator.page(page)
        return render(request, 'blog/home.html', {
            "page_obj":page_obj,
        })


class AboutPageView(TemplateView):
    template_name = "blog/about.html"
    

class PostDetailPageView(View):
    def get(self, request, id):
        posts = Post.objects.get(id=id)
        return render(request, 'blog/post_detail.html', {
            "post":posts,
            "user_posts":""
        })


class UserProfilePageView(LoginRequiredMixin, View):
    def get(self, request):

        posts  = Post.objects.filter(author=request.user)

        return render(request, 'blog/user_posts.html', {
            "posts":posts,
        })


class PostFormPageView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "blog/post_form.html", {"form":PostCreateForm()})
    
    def post(self, request):
        form = PostCreateForm(request.POST)

        if form.is_valid():
          
            post = Post.objects.create(
                title        = form.cleaned_data.get('title'),
                content      = form.cleaned_data.get('content'),
                is_active    = form.cleaned_data.get('is_active'),
                author       = request.user, 
                publisher_at = datetime.datetime.now().strftime('%Y-%m-%d'))
            post.save()

            messages.success(request, "Post succesfully created")
            return redirect('home')
        messages.warning(request, "There is a mistake in your post ! or your post is not filled to the depth.")
        return render(request, "blog/post_form.html", {"form":form})


class UserPostPageView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = 'posts'

@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            messages.success(request, "Post succsessfully updated")
            form.save()
            return redirect("profile")

        messages.error(request, "You`r post is not valid !")
        return render(request, "blog/post_update.html", {"form":form})
    
    form = PostUpdateForm(instance=post)
    return render(request, "blog/post_update.html", {
        "form":form,
        "post":post
        })
    

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        messages.success(request, "post successfully deleted")
        post.delete()
        return redirect("profile")
    return render(request, "blog/post_confirm_delete.html", {"post":post})