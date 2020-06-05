from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.api_root),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),

    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name='category-detail'),

    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>', views.AuthorDetail.as_view(), name='author-detail'),

    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name='comment-detail'),

    path('mailingmembers/', views.MailingMemberList.as_view(), name='mailingmember-list'),
    path('mailingmembers/<int:pk>', views.MailingMemberDetail.as_view(), name='mailingmember-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)