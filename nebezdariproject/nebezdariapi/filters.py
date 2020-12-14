import rest_framework_filters as filters
from nebezdariapp.models import *


class CategoryFilter(filters.FilterSet):
    '''
    Фильтр для категорий
        по полю Название категории(name):
            exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'
    '''
    class Meta:
        model = Category
        fields = {'name': ['exact', 'in', 'startswith']}

class CommentFilter(filters.FilterSet):
    '''
    Фильтр для комментариев
        по полю Имя автора комментария (name):
            exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'
    '''
    class Meta:
        model = Comment
        fields = {'name': ['exact', 'in', 'startswith']}

class AuthorFilter(filters.FilterSet):
    '''
     Фильтр для авторов
        по полю Логин автора (username):
            exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'

        по полю Имя автора (first_name):
            exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'

        по полю Фамилия автора (last_name):
            exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'
     '''
    class Meta:
        model = Author
        fields = {
            'username': ['exact', 'in', 'startswith'],
            'first_name': ['exact', 'in', 'startswith'],
            'last_name': ['exact', 'in', 'startswith'],
        }

class MailingMemberFilter(filters.FilterSet):
    '''
        Фильтр для подписчиков по E-Mail
            по полю E-Mail подписчика (email):
                exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'
    '''
    class Meta:
        model = MailingMember
        fields = {'email': ['exact', 'in', 'startswith']}

class PostFilter(filters.FilterSet):
    '''
        Фильтр для постов
            по полю Название поста (title):
                exact - 'Точное совпадение', in - 'Содержит', startswith - 'Начинается с'
    '''

    category = filters.RelatedFilter(CategoryFilter, field_name='categories', queryset=Category.objects.all())
    comment = filters.RelatedFilter(CommentFilter, field_name='comments', queryset=Comment.objects.all())
    author = filters.RelatedFilter(AuthorFilter, field_name='author', queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = {
            'title': ['exact', 'in', 'startswith']
        }