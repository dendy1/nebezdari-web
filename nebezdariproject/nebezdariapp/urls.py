from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('login/', views.user_login, name='login'),
    path('author/login/', views.user_login, name='login'),
    path('admin/login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),
    path('author/logout/', views.user_logout, name='logout'),
    path('admin/logout/', views.user_logout, name='logout'),

    path('author/<username>/', views.author, name='author'),
    path('author/<username>/edit', views.edit_author, name='edit_author'),
    path('author/addpost/', views.add_post, name='add_post'),
    path('author/editpost/', views.edit_post, name='edit_post'),

    path('admin/adduser', views.admin_add_user, name='admin_add_user'),
    path('admin/authors', views.admin_authors, name='admin_all_users'),
    path('admin/posts', views.admin_all_posts, name='admin_all_posts'),
]