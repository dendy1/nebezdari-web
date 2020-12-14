from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from nebezdariapp.models import *

class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для категорий, который позволяет получать и отправлять информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на категорию
    'id' - ID категории
    'name' - Название категории
    """
    class Meta:
        model = Category
        fields = ('url', 'id', 'name')
        extra_kwargs = {
            'name': {'validators': []},
        }

class AuthorDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для автора, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на автора
    'id' - ID автора
    'username' - Логин автора
    'first_name' - Имя автора
    'last_name' - Фамилия автора
    'email' - E-Mail автора
    'avatar' - Ссылка на местоположение аватара автора
    """

    url = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    avatar = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'avatar')
        extra_kwargs = {
            'username': {'validators': []},
        }

class PostListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для постов, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на пост
    'id' - ID поста
    'title' - Название поста
    """

    class Meta:
        model = Post
        fields = ('url', 'id', 'title')

class CommentListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для комментариев, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на комментарий
    'id' - ID комментария
    'author' - ID пользователя, кому принадлежит комментарий
    'name' - Имя пользователя, если комментарий оставил гость
    'text' - Текст комментария
    'created_at' - Дата создания комментария
    'parent' - ID родительского комментария, если данный комментарий является ответом на другой
    """

    class Meta:
        model = Comment
        fields = ('url', 'id', 'author', 'name', 'text', 'created_at', 'parent')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для автора, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на автора
    'id' - ID автора
    'username' - Логин автора
    'first_name' - Имя автора
    'last_name' - Фамилия автора
    'email' - E-Mail автора
    'about' - Информация об авторе
    'avatar' - Ссылка на местоположение аватара автора
    'last_login' - Дата последнего входа автора
    'posts' - Информация о постах, принадлежащих данному автору (вложенный запрос)
    """
    posts = PostListSerializer(read_only=True, many=True)

    class Meta:
        model = Author
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'about', 'avatar', 'last_login', 'posts')

class MailingMemberSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для подписчиков по E-Mail, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на подписчика
    'id' - ID подписчика
    'email' - E-Mail подписчика
    """
    class Meta:
        model = MailingMember
        fields = ('url', 'id', 'email')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для категорий, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на категорию
    'id' - ID категории
    'name' - Название категории
    'posts' - Информация о постах, принадлежащих данной категории (вложенный запрос)
    """

    posts = PostListSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'posts')
        extra_kwargs = {
            'name': {'validators': []},
        }

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для комментариев, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на комментарий
    'id' - ID комментария
    'author' - ID пользователя, кому принадлежит комментарий
    'name' - Имя пользователя, если комментарий оставил гость
    'text' - Текст комментария
    'created_at' - Дата создания комментария
    'parent' - ID родительского комментария, если данный комментарий является ответом на другой
    'author' - Информация об авторе, который является автором комментария (вложенный запрос)
    'post' - Информация о посте, в котором оставлен комментарий (вложенный запрос)
    """

    author = AuthorDetailSerializer(required=False, allow_null=True)
    post = PostListSerializer(read_only=True)

    def create(self, validated_data):
        author_validated_data = validated_data.pop('author')
        post_validated_data = validated_data.pop('post')
        post = get_object_or_404(Post, **post_validated_data)

        comment = Comment.objects.create(**validated_data)
        comment.post = post

        author = None
        if author_validated_data is not None:
            try:
                author = Author.objects.get(**author_validated_data)
            except Author.DoesNotExist:
                pass
        comment.author = author

        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ('url', 'id', 'post', 'author', 'name', 'text', 'created_at', 'parent')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для постов, который позволяет получать информацию в виде JSON и XML, содержащую поля
    'url' - Ссылка на пост
    'id' - ID поста
    'title' - Название поста
    'text' - Текст поста
    'author' - Информация об авторе, который является автором поста (вложенный запрос)
    'categories' - Информация о категориях, к которым принадлежит пост (вложенный запрос)
    'comments' - Информация о комментариях, оставленных под данным постом (вложенный запрос)
    'posted_at' - Дата опубликования статьи
    'edited_at' - Дата последнего изменеия статьи
    'image' - Ссылка на изображение-превью поста
    """

    author = AuthorDetailSerializer()
    categories = CategoryListSerializer(many=True)
    comments = CommentListSerializer(many=True, read_only=True)
    posted_at = serializers.DateTimeField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        categories_validated_data = validated_data.pop('categories')
        author_validated_data = validated_data.pop('author')
        author = get_object_or_404(Author, **author_validated_data)

        post = Post.objects.create(**validated_data)
        post.author = author

        for category_data in categories_validated_data:
            category, created = Category.objects.get_or_create(**category_data)
            post.categories.add(category)

        return post

    def update(self, instance, validated_data):
        categories_validated_data = validated_data.pop('categories')

        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.author = validated_data.get('author', instance.author)
        instance.edited_at = validated_data.get('edited_at', instance.edited_at)
        instance.categories.clear()

        for category_data in categories_validated_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)

        instance.save()

        return instance

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'text', 'author', 'categories', 'comments', 'posted_at', 'edited_at', 'image')