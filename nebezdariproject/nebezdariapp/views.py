from django.shortcuts import HttpResponse, render
from .models import Categories, Posts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    index_categories_count = 10
    posts_per_page = 5
    categories_list = Categories.objects.all()[:index_categories_count]
    posts_list = Posts.objects.all()
    page_num = request.GET.get('page')
    paginator = Paginator(posts_list, per_page=posts_per_page)
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'main-page.html',
                  context={'categories_list': categories_list,
                           'posts': posts,})


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