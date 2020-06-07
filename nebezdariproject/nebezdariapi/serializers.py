from rest_framework import serializers
from nebezdariapp.models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'about', 'avatar', 'last_login')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'id', 'name')
        extra_kwargs = {
            'name': {'validators': []},
        }

class MailingMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingMember
        fields = ('url', 'id', 'email')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'id', 'post', 'author', 'name', 'text', 'created_at', 'parent')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    categories = CategorySerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    posted_at = serializers.DateTimeField(read_only=True)
    edited_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        categories_validated_data = validated_data.pop('categories')
        post = Post.objects.create(**validated_data)

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