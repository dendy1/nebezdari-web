from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import NestedViewSetMixin

from nebezdariapi.filters import *
from nebezdariapi.serializers import *
from nebezdariapp.models import *

# Точка входа в API для всех возможных методов
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def api_root(request, format=None):
    return Response({
        'posts': reverse('post-list', request=request, format=format),
        'categories' : reverse('category-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
        'mailingmembers': reverse('mailingmember-list', request=request, format=format)
    })


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления логикой, связанной с постами
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_class = PostFilter

class CategoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления логикой, связанной с категориями
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_class = CategoryFilter

class AuthorViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления логикой, связанной с авторами
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filter_class = AuthorFilter

class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления логикой, связанной с комментариями
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_class = CommentFilter

class MailingMemberViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления логикой, связанной с подписчиками по E-Mail
    """
    serializer_class = MailingMemberSerializer      #
    queryset = MailingMember.objects.all()
    filter_class = MailingMemberFilter              # Возможность фильтрации