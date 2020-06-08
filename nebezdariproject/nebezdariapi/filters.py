import rest_framework_filters as filters
from nebezdariapp.models import *


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {'name': ['exact', 'in', 'startswith']}

class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = {'name': ['exact', 'in', 'startswith']}

class AuthorFilter(filters.FilterSet):
    class Meta:
        model = Author
        fields = {
            'username': ['exact', 'in', 'startswith'],
            'first_name': ['exact', 'in', 'startswith'],
            'last_name': ['exact', 'in', 'startswith'],
        }

class MailingMemberFilter(filters.FilterSet):
    class Meta:
        model = MailingMember
        fields = {'email': ['exact', 'in', 'startswith']}

class PostFilter(filters.FilterSet):
    category = filters.RelatedFilter(CategoryFilter, field_name='categories', queryset=Category.objects.all())
    comment = filters.RelatedFilter(CommentFilter, field_name='comments', queryset=Comment.objects.all())
    author = filters.RelatedFilter(AuthorFilter, field_name='author', queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = {
            'title': ['exact', 'in', 'startswith']
        }