from django.contrib import admin

from .models import Author, Category, Comment, Post, MailingMember

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(MailingMember)