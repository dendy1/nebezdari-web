from django.conf.urls import url
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter
from .views import *

router = ExtendedSimpleRouter()
posts_routers = router.register(r'posts', PostViewSet, basename='post')
posts_routers.register(
    r'comments',
    CommentViewSet,
    basename='post-comment',
    parents_query_lookups=['post']
)
posts_routers.register(
    r'categories',
    CategoryViewSet,
    basename='post-category',
    parents_query_lookups=['post']
)

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'mailingmembers', MailingMemberViewSet, basename='mailingmember')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'author', AuthorViewSet, basename='author')

urlpatterns = [
    path('', api_root),
    url(r'^', include(router.urls)),
]