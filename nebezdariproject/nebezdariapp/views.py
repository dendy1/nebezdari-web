from django.shortcuts import HttpResponse, render, HttpResponseRedirect, get_object_or_404, get_list_or_404, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .lib.custom_paginator import CustomPaginator
from .models import Category, Post, Author, Comment
from django.core.mail import send_mail, BadHeaderError
from .forms import PostForm, LoginForm, NewAuthorForm, ContactForm, EditAuthorForm


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

def about(request):
    return render(request,
                  'blog/about-page.html',
                  context={})

def contact(request):
    if request.method == "POST":
        destination_mail = ["admin@nebezdari.ru",]
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

            return render(request, 'blog/thanks-page.html', context={})

    else:
        form = ContactForm()
    return render(request,
                  'blog/contact-page.html',
                  context={})

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/author')

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
                        return HttpResponseRedirect('/author/' + user.username)
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()

    return render(request,
                  'blog/login-page.html',
                  context={'form': form})

@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def post(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter()
    related_posts = Post.objects.all()
    return render(request,
                  'blog/post-page.html',
                  context={'post':post, 'id':id, 'comment_list':comments, 'related_post_list':related_posts})

@login_required(login_url='/login')
def post_add(request):
    if request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return HttpResponseRedirect('/author/')
    else:
        form = PostForm()

    return render(request,
                  'author/add-post-page.html',
                  context={'form': form})

@login_required(login_url='/login')
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if not request.user.is_authenticated or request.user.is_superuser or request.user.username != post.author.username:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return HttpResponseRedirect('/author/')
    else:
        form = PostForm(instance=post)

    return render(request,
                  'author/edit-post-page.html',
                  context={'form': form, 'id':id})

@login_required(login_url='/login')
def admin(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    return render(request,
                  'admin/admin-main-page.html',
                  context={})

@login_required(login_url='/login')
def admin_user_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url='/login')
def admin_authors(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    author_list = Author.objects.all()
    return render(request,
                  'admin/admin-authors-page.html',
                  context={'author_list':author_list})

@login_required(login_url='/login')
def admin_posts(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    posts_list = Post.objects.all()
    return render(request,
                  'admin/admin-posts-page.html',
                  context={'posts_list':posts_list})

@login_required(login_url='/login')
def admin_reset_password(request, username):
    if not request.user.is_superuser:
        raise PermissionDenied

    user = get_object_or_404(Author, username=username)


@login_required(login_url='/login')
def admin_user_delete(request, username):
    if not request.user.is_superuser:
        raise PermissionDenied

    user = get_object_or_404(Author, username=username)


def author(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        return HttpResponseRedirect('/author/' + request.user.username)

    raise Http404("Проверьте правильность пути")

def author_page(request, username):
    author = get_object_or_404(Author, username=username)
    post_list = Post.objects.filter(author=author)
    return render(request,
                  'blog/author-page.html',
                  context={'author': author,
                           'post_list': post_list})

@login_required(login_url='/login')
def author_edit(request, username):
    if not request.user.is_superuser and request.user.username != username:
        raise PermissionDenied

    author = get_object_or_404(Author, username=username)
    if request.method == "POST":
        form = EditAuthorForm(request.POST, request.FILES)
        if form.is_valid():
            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.about = form.cleaned_data['about']
            author.avatar = form.cleaned_data['avatar']
            author.save()
            return HttpResponseRedirect('/author/' + username)
    else:
        form = EditAuthorForm(instance=author)

    return render(request,
                  'author/edit-author-page.html',
                  context={'form':form, 'username':username})

def error(request):
    return render(request,
                  'errors/404.html',
                  context={})