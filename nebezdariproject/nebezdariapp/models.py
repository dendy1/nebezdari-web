from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models

class MailingMember(models.Model):
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "nebezdariapp_mailing_members"

class Author(AbstractUser):
    about = models.CharField(max_length=2047, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='posts')
    title = models.CharField(max_length=256)
    text = RichTextUploadingField()
    categories = models.ManyToManyField(Category, related_name='posts')
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null=True, related_name='comments')
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=512)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text