from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from nebezdariapp.models import *

class CategorySerializerForPost(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'id', 'name')
        extra_kwargs = {
            'name': {'validators': []},
        }

class AuthorSerializerForPost(serializers.HyperlinkedModelSerializer):
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

class PostSerializerForComment(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=False, required=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'title')

class PostSerializerForCategory(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'id', 'title')

class PostSerializerForAuthor(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'id', 'title')

class CommentSerializerForPost(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'id', 'author', 'name', 'text', 'created_at', 'parent')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializerForAuthor(many=True)

    class Meta:
        model = Author
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'about', 'avatar', 'last_login', 'posts')

class MailingMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MailingMember
        fields = ('url', 'id', 'email')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializerForCategory(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'posts')
        extra_kwargs = {
            'name': {'validators': []},
        }

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializerForPost(required=False, allow_null=True)
    post = PostSerializerForComment()

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
    author = AuthorSerializerForPost()
    categories = CategorySerializerForPost(many=True)
    comments = CommentSerializerForPost(many=True, read_only=True)
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