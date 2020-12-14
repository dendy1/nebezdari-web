from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import HttpResponse, render, HttpResponseRedirect, get_object_or_404

from nebezdariapp.forms import NewAuthorForm
from nebezdariapp.models import Author, Post


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