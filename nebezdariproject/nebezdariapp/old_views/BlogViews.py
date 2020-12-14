from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from nebezdariapp.forms import CategoriesForm, ContactForm, SubscribeForm
from nebezdariapp.lib.custom_paginator import CustomPaginator
from nebezdariapp.models import Post, Category, MailingMember


def index(request):
    categories_form = CategoriesForm(request.GET)
    if request.method == 'GET':
        if categories_form.is_valid():
            categories = categories_form.cleaned_data['categories']
            if not categories:
                posts_list = Post.objects.all().order_by('-posted_at')
            else:
                posts_list = Post.objects.filter(categories__in=categories).distinct().order_by('-posted_at')
        else:
            posts_list = Post.objects.all().order_by('posted_at')
    else:
        posts_list = Post.objects.all().order_by('posted_at')

    index_categories_count = 10 #count of categories in categories bar
    posts_per_page = 5 #count of posts on page
    pagination_pages_range = 2 #count of pages right and left to the current page
    categories_list = Category.objects.all()[:index_categories_count]
    page_num = request.GET.get('page')
    paginator = CustomPaginator(posts_list, posts_per_page, pagination_pages_range)

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    pagination_list = paginator.pagination_list(page_num)

    return render(request,
                  'blog/main-page.html',
                  context={'categories_list': categories_list,
                           'posts': posts,
                           'pagination_list': pagination_list,
                           'categories_form': categories_form})

def about(request):
    return render(request,
                  'blog/about-page.html',
                  context={})

def contact(request):
    if request.method == "POST":
        destination_mail = ["admin@nebezdari.ru", ]
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']

            final_message = "Name: " + name + ", email: " + sender + ", Text: " + message
            try:
                send_mail(subject, final_message, 'noreply@nebezdari.ru', destination_mail)
            except BadHeaderError:
                return HttpResponse('Invalid header found')

            return render(request, 'blog/thanks-page.html', context={
                'redirect_to':'/',
                'redirect_time': 5 #in seconds
            })
    else:
        form = ContactForm()
    return render(request,
                  'blog/contact-page.html',
                  context={"form": form})

def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mailing_member = MailingMember(email=email)
            mailing_member.save()

    return HttpResponseRedirect('/')