from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('author', views.author, name='author'),
    path('login', views.login, name='login'),
]