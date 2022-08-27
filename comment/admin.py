from django.contrib import admin
from .models import Comment

# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'body', 'created']
    list_filter = ['post', 'created', 'user']
    search_fields = ['body']