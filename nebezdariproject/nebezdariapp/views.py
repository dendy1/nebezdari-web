from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from .lib.custom_paginator import CustomPaginator
from .models import Category, Post, Author
from .forms import PostForm, LoginForm, NewAuthorForm


def index(request):
    index_categories_count = 10 #count of categories in categories bar
    posts_per_page = 5 #count of posts on page
    pagination_pages_range = 2 #count of pages right and left to the current page
    categories_list = Category.objects.all()[:index_categories_count]
    posts_list = Post.objects.all()
    page_num = request.GET.get('page')
    paginator = CustomPaginator(posts_list, posts_per_page, pagination_pages_range)
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    pagination_list = paginator.pagination_list()

    return render(request,
                  'blog/main-page.html',
                  context={'categories_list': categories_list,
                           'posts': posts,
                           'pagination_list': pagination_list, })


def post(request):
    return render(request,
                  'blog/post-page.html',
                  context={})

def about(request):
    return render(request,
                  'blog/about-page.html',
                  context={})

def contact(request):
    return render(request,
                  'blog/contact-page.html',
                  context={})

def author(request, username):
    author = Author.objects.get(username=username)
    post_list = Post.objects.filter(author=author)
    if author is not None:
        return render(request,
                      'blog/author-page.html',
                      context={'author':author,
                               'post_list':post_list})

    return HttpResponseRedirect('/')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            print(user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect('/admin')
                    else:
                        return HttpResponseRedirect('/author')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()

    return render(request,
                  'blog/login-page.html',
                  context={'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                author=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'])

            post.save()
            for category in form.cleaned_data['categories']:
                post.categories.add(category)
            post.save()

            return HttpResponseRedirect('/')
    else:
        form = PostForm()

    return render(request,
                  'author/add-post-page.html',
                  context={'form': form})

def edit_post(request):
    form = PostForm()
    context = {
        "form": form
    }
    return render(request, 'author/edit-post-page.html', context)

def admin_add_user(request):
    if request.method == 'POST':
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            password = Author.objects.make_random_password(length=10)
            print(password)
            author = Author.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                password
            )

            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.is_active = True
            author.save()
            return HttpResponseRedirect('/admin/authors')
    else:
        form = NewAuthorForm()

    return render(request,
                  'admin/admin-add-user-page.html',
                  context={'form':form})

def admin_authors(request):
    author_list = Author.objects.all()

    return render(request,
                  'admin/admin-authors-page.html',
                  context={'author_list':author_list})

def admin_all_posts(request):
    form = PostForm()
    context = {
        "form": form
    }
    return render(request, 'admin/admin-posts-page.html', context)