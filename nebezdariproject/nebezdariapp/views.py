from django.shortcuts import HttpResponse, render
from django.template import loader
from nebezdariapp.forms import PostForm
# Create your views here.


def index(request):
    template = loader.get_template('main-page.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def post(request):
    template = loader.get_template('post-page.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('about-page.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template('contact-page.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def author(request):
    template = loader.get_template('author-page.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('login-page.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def add_post(request):
    form = PostForm()
    context = {
        "form" : form
    }
    return render(request, 'add-post-page.html', context)

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