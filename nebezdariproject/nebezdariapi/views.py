from rest_framework import mixins, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_extensions.mixins import NestedViewSetMixin

from nebezdariapi.serializers import *
from nebezdariapi.filters import *
from nebezdariapp.models import *

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'posts': reverse('post-list', request=request, format=format),
        'categories' : reverse('category-list', request=request, format=format),
        'authors': reverse('author-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format),
        'mailingmembers': reverse('mailingmember-list', request=request, format=format)
    })

class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_class = PostFilter

class CategoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_class = CategoryFilter

class AuthorViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filter_class = AuthorFilter

class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_class = CommentFilter

class MailingMemberViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = MailingMemberSerializer
    queryset = MailingMember.objects.all()
    filter_class = MailingMemberFilter