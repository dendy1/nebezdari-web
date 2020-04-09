from django.shortcuts import HttpResponse, render
from django.template import loader
from .models import Categories, Posts


# Create your views here.
def index(request):
    index_categories_count = 10
    categories_list = Categories.objects.all()[:index_categories_count]
    posts_list = Posts.objects.all()
    return render(request,
                  'main-page.html',
                  context={'categories_list': categories_list,
                           'posts_list': posts_list})

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