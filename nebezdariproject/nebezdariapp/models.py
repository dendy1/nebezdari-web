from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models

class MailingMember(models.Model):
    """
    Сущность "Подписчик по E-mail"
    """
    email = models.EmailField(max_length=255)       # E-Mail подписчика

    def __str__(self):
        return self.email

    class Meta:
        db_table = "nebezdariapp_mailing_members"

class Author(AbstractUser):
    """
    Сущность "Автора статьи"
    """
    about = models.CharField(max_length=2047, blank=True, default='')           # Личная информация об авторе
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)     # Ссылка на изобрадение-аватар

    def __str__(self):
        return self.username

class Category(models.Model):
    """
    Сущность "Категория статьи"
    """
    name = models.CharField(max_length=64, unique=True)     # Название категории

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Сущность "Статья"
    """
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='posts')      # Автора статьи (внешний ключ)
    title = models.CharField(max_length=256)                                                            # Заголовок статьи
    text = RichTextUploadingField()                                                                     # Текст статьи
    categories = models.ManyToManyField(Category, related_name='posts')                                 # Категории статьи (M2M)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)                                # Ссылка на изображение-превью
    posted_at = models.DateTimeField(auto_now_add=True)                                                 # Дата публикации статьи
    edited_at = models.DateTimeField(auto_now_add=True)                                                 # Дата последнего редактирования статьи

    def comments_count(self):
        """
        Метод, возвращающий количество комментариев, опубликованных под статьей
        """
        return self.comments.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Сущность "Комментарий статьи"
    """
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null=True, related_name='comments')
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=512)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text