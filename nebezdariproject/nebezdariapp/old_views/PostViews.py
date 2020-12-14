from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from nebezdariapp.forms import PostForm, CommentForm
from nebezdariapp.lib.mail.mass_mailing import subscribers_mass_mail
from nebezdariapp.models import Post, Comment


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

def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)

    if (request.user == post.author or request.user.is_staff):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return HttpResponseRedirect('/post/' + str(post.id))
    else:
        return HttpResponseForbidden()

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