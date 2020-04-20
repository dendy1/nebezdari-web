from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.user_login, name='login'),
    path('author/login/', views.user_login, name='login'),
    path('admin/login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),
    path('author/logout/', views.user_logout, name='logout'),
    path('admin/logout/', views.user_logout, name='logout'),

    path('author/', views.author, name='default_author'),
    path('author/<username>/', views.author_page, name='author'),
    path('author/<username>/edit/', views.author_edit, name='author'),

    path('post/add/', views.post_add, name='add_post'),
    path('post/<id>/', views.post, name='post'),
    path('post/<id>/edit/', views.post_edit, name='edit_post'),
    path('post/<id>/delete/', views.post_delete, name='delete_post'),

    path('admin/', views.admin, name='Admin'),
    path('admin/user/add/', views.admin_user_add, name='admin_add_user'),
    path('admin/user/<username>/resetpassword/', views.admin_reset_password, name='Reset password for user'),
    path('admin/user/<username>/delete/', views.admin_user_delete, name='Delete user'),
    path('admin/users/', views.admin_authors, name='admin_all_users'),
    path('admin/posts/', views.admin_posts, name='admin_all_posts'),

    path('error/', views.error, name='admin_all_posts'),
]