from django.contrib import admin
from .models import Post, Category

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created", "published"]
    list_filter = ["user", "created", "published", "tags"]
    list_per_page = 20
    search_fields = ("title", "body", "user")
    date_hierarchy = "created"
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["title", "slug", "available"]
    list_filter = ["title", "available"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
