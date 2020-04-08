from django.shortcuts import HttpResponse
from django.template import loader


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