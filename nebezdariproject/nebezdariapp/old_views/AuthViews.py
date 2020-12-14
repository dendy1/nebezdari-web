from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render, HttpResponseRedirect

from nebezdariapp.forms import LoginForm


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