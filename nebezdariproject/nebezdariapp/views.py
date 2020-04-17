from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from .models import Category, Post
from django.core.paginator import EmptyPage, PageNotAnInteger
from .lib.custom_paginator import CustomPaginator
from .forms import PostForm


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
                  'main-page.html',
                  context={'categories_list': categories_list,
                           'posts': posts,
                           'pagination_list': pagination_list, })


def post(request):
    return render(request,
                  'post-page.html',
                  context={})

def about(request):
    return render(request,
                  'about-page.html',
                  context={})

def contact(request):
    return render(request,
                  'contact-page.html',
                  context={})

def author(request):
    return render(request,
                  'author-page.html',
                  context={})

def login(request):
    return render(request,
                  'author-page.html',
                  context={})   

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
                  'add-post-page.html',
                  context={'form': form})

def edit_post(request):
    form = PostForm()
    context = {
        "form": form
    }
    return render(request, 'edit-post-page.html', context)

def admin_all_posts(request):
    form = PostForm()
    context = {
        "form": form
    }
    return render(request, 'admin-all-posts-page.html', context)

def admin_add_user(request):
    context = {
    }
    return render(request, 'admin-add-user-page.html', context)

def admin_all_users(request):
    context = {
    }
    return render(request, 'admin-all-users-page.html', context)
