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
    comments = CommentSerializer(many=True)

    def create(self, validated_data):
        categories_validated_data = validated_data.pop('categories')
        comments_validated_data = validated_data.pop('comments')

        post = Post.objects.create(**validated_data)

        for category_data in categories_validated_data:
            category = Category.objects.create(post=post, **category_data)
            post.categories.add(category)

        for comment_data in comments_validated_data:
            Comment.objects.create(post=post, **comment_data)

        return post

    def update(self, instance, validated_data):
        categories_validated_data = validated_data.pop('categories')
        comments_validated_data = validated_data.pop('comments')

        for category_data in categories_validated_data:
            Category.objects.update_or_create(**category_data)

        for comment_data in comments_validated_data:
            Comment.objects.update_or_create(**comment_data)

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'text', 'author', 'categories', 'comments', 'posted_at', 'edited_at', 'image')