from django.contrib import admin

from .models import Author, Category, Comment, Post, MailingMember

admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(MailingMember)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    autocomplete_fields = ['categories']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']