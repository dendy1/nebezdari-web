from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, Http404

from nebezdariapp.forms import EditAuthorForm
from nebezdariapp.models import Post, Author


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