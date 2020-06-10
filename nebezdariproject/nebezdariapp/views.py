from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponse, render, HttpResponseRedirect, get_object_or_404, get_list_or_404, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied

from .lib.custom_paginator import CustomPaginator
from .lib.mail.mass_mailing import subscribers_mass_mail
from .models import Category, Post, Author, Comment, MailingMember
from django.core.mail import send_mass_mail, send_mail, BadHeaderError
from .forms import PostForm, LoginForm, NewAuthorForm, ContactForm, EditAuthorForm, SubscribeForm, CategoriesForm, CommentForm


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
    posts_per_page = 2 #count of posts on page
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

def post(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter()
    related_posts = Post.objects.all()
    commentForm = CommentForm(request.POST or None)
    if commentForm.is_valid():
        comment = commentForm.save(commit=False)
        comment.post = post
        if request.user.is_authenticated:
            comment.author = request.user

        try:
            comment.parent = Comment.objects.get(id=commentForm.cleaned_data['parent_comment'])
        except Comment.DoesNotExist:
            comment.parent = None

        comment.save()
        return HttpResponseRedirect(request.path_info)
    return render(request,
                  'blog/post-page.html',
                  context={'post':post,
                           'comment_list':comments,
                           'related_post_list':related_posts,
                           'commentForm':commentForm})

def author(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
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

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/author')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
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
    return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def post_add(request):
    if request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            subscribers_message = "Вышел новый пост: "
            link = "https://www.nebezdari.ru/post/" + str(post.id)
            subscribers_mass_mail(subscribers_message, link=link)

            return HttpResponseRedirect('/author/')
    else:
        form = PostForm()

    return render(request,
                  'author/add-post-page.html',
                  context={'form': form})

@login_required(login_url='/login')
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user.username != post.author.username:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
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
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if not request.user.is_staff or (post.author != None and request.user.username != post.author.username):
        raise PermissionDenied

    Post.delete(post)

    if request.user.is_staff:
        return HttpResponseRedirect('/admin/posts/')
    else:
        return HttpResponseRedirect('/author/')

@login_required(login_url='/login')
def author_edit(request, username):
    if not request.user.is_staff and request.user.username != username:
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

@staff_member_required
def admin(request):
    return render(request,
                  'admin/admin-main-page.html',
                  context={})

@staff_member_required
def admin_user_add(request):
    if request.method == 'POST':
        form = NewAuthorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = Author.objects.make_random_password(length=10)

            subject = username + ". Регистрация на nebezdari.ru"
            message = "На ваш E-Mail адрес был зарегистрирован аккаунт на сайте nebezdari.ru" + "\nЛогин: " + username + "\nПароль: " + password
            destination_mail = [email, ]

            try:
                send_mail(subject, message, 'noreply@nebezdari.ru', destination_mail)

                author = Author.objects.create_user(
                    username,
                    email,
                    password
                )

                author.first_name = form.cleaned_data['first_name']
                author.last_name = form.cleaned_data['last_name']
                author.is_active = True
                author.save()

                return HttpResponseRedirect('/admin/users/')
            except BadHeaderError:
                return HttpResponse('Invalid header found')
    else:
        form = NewAuthorForm()

    return render(request,
                  'admin/admin-add-user-page.html',
                  context={'form':form})

@staff_member_required
def admin_authors(request):
    author_list = Author.objects.filter(is_staff=False)
    return render(request,
                  'admin/admin-authors-page.html',
                  context={'author_list':author_list})

@staff_member_required
def admin_posts(request):
    posts_list = Post.objects.all()
    return render(request,
                  'admin/admin-posts-page.html',
                  context={'posts_list':posts_list})

@staff_member_required
def admin_reset_password(request, username):
    user = get_object_or_404(Author, username=username)
    password = Author.objects.make_random_password(length=10)

    subject = user.username + ". Новый пароль на nebezdari.ru"
    message = "Ваш новый пароль: " + password
    destination_mail = [user.email, ]

    try:
        send_mail(subject, message, 'noreply@nebezdari.ru', destination_mail)
        user.set_password(password)
        user.save()
        return HttpResponseRedirect('/admin/users/')
    except BadHeaderError:
        return HttpResponse('Invalid header found')

@staff_member_required
def admin_user_delete(request, username):
    user = get_object_or_404(Author, username=username)
    Author.delete(user)
    return HttpResponseRedirect('/admin/users/')

def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mailing_member = MailingMember(email=email)
            mailing_member.save()

    return HttpResponseRedirect('/')

def error_400(request, exception):
    data = {}
    return render(request, 'errors/400.html', data)

def error_403(request, exception):
    data = {}
    return render(request, 'errors/403.html', data)

def error_404(request, exception):
    data = {}
    return render(request, 'errors/404.html', data)

def error_500(request):
    data = {}
    return render(request, 'errors/500.html', data)

def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)

    if (request.user == post.author or request.user.is_staff):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return HttpResponseRedirect('/post/' + str(post.id))
    else:
        return HttpResponseForbidden()