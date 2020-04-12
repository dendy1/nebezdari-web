from django.shortcuts import HttpResponse, render
from .models import Categories, Posts
from django.core.paginator import EmptyPage, PageNotAnInteger
from .lib.custom_paginator import CustomPaginator


# Create your views here.
def index(request):
    index_categories_count = 10 #count of categories in categories bar
    posts_per_page = 5 #count of posts on page
    pagination_pages_range = 2 #count of pages right and left to the current page
    categories_list = Categories.objects.all()[:index_categories_count]
    posts_list = Posts.objects.all()
    page_num = int(request.GET.get('page'))
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