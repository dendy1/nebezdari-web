from django.urls import include, path
from rest_framework_extensions.routers import ExtendedSimpleRouter
from .views import *

# Используем расширенный роутер (из библиотеки rest_framework_extensions),
# позволяющий регистрировать ссылки на вложенные запросы
router = ExtendedSimpleRouter()

# Регистрация запросов вида
# /posts/
# /posts/{post_id}
posts_routers = router.register(r'posts', PostViewSet, basename='post')

# Регистрация вложенный запросов вида
# /posts/{post_id}/comments/
# /posts/{post_id}/comments/{comment_id}/
posts_routers.register(
    'comments',
    CommentViewSet,
    basename='post-comment',
    parents_query_lookups=['post']
)

# Регистрация вложенный запросов вида
# /posts/{post_id}/categories/
# /posts/{post_id}/categories/{category_id}/
posts_routers.register(
    'categories',
    CategoryViewSet,
    basename='post-category',
    parents_query_lookups=['post']
)

# Регистрация запросов вида
# /categories/
# /categories/{category_id}
router.register('categories', CategoryViewSet, basename='category')

# Регистрация запросов вида
# /mailingmembers/
# /mailingmembers/{mailingmember_id}
router.register('mailingmembers', MailingMemberViewSet, basename='mailingmember')

# Регистрация запросов вида
# /comments/
# /comments/{comment_id}
router.register('comments', CommentViewSet, basename='comment')

# Регистрация запросов вида
# /authors/
# /authors/{author_id}
router.register('authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('', include(router.urls)),
]