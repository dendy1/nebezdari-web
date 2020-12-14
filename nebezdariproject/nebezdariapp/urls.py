from django.urls import path

from nebezdariapp.old_views import AdminViews, AuthorViews, AuthViews, BlogViews, PostViews

urlpatterns = [
    path('', BlogViews.index, name='index'),
    path('contact/', BlogViews.contact, name='contact'),
    path('about/', BlogViews.about, name='about'),
    path('subscribe/', BlogViews.subscribe, name='subscribe'),

    path('login/', AuthViews.user_login, name='login'),
    path('author/login/', AuthViews.user_login, name='login'),
    path('admin/login/', AuthViews.user_login, name='login'),

    path('logout/', AuthViews.user_logout, name='logout'),
    path('author/logout/', AuthViews.user_logout, name='logout'),
    path('admin/logout/', AuthViews.user_logout, name='logout'),

    path('author/', AuthorViews.author, name='default_author'),
    path('author/<username>/', AuthorViews.author_page, name='author'),
    path('author/<username>/edit/', AuthorViews.author_edit, name='author'),

    path('post/add/', PostViews.post_add, name='add_post'),
    path('post/<id>/', PostViews.post, name='post'),
    path('post/<id>/edit/', PostViews.post_edit, name='edit_post'),
    path('post/<id>/delete/', PostViews.post_delete, name='delete_post'),
    path('post/<int:post_id>/deletecomment/<int:comment_id>/', PostViews.delete_comment, name='delete-comment'),

    path('admin/', AdminViews.admin, name='Admin'),
    path('admin/user/add/', AdminViews.admin_user_add, name='admin_add_user'),
    path('admin/user/<username>/resetpassword/', AdminViews.admin_reset_password, name='Reset password for user'),
    path('admin/user/<username>/delete/', AdminViews.admin_user_delete, name='Delete user'),
    path('admin/users/', AdminViews.admin_authors, name='admin_all_users'),
    path('admin/posts/', AdminViews.admin_posts, name='admin_all_posts'),
]