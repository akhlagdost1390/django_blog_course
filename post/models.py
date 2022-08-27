from django.db import models
from django.conf import settings
from django.urls import reverse
from tagging.fields import TagField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


# create your manager here


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True, category__available=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    available = models.BooleanField(default=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, "posts")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    banner = models.ImageField(blank=True, upload_to="posts/%Y/%m/%d/")
    tags = TagField(blank=True)
    

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, "likes", blank=True)
    likes = models.PositiveIntegerField(default=0)

    # managers
    objects = models.Manager()
    available_posts = PostManager()

    def get_absolute_url(self):
        return reverse(
            "post:detail", kwargs={"category": self.category, "slug": self.slug}
        )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


# signals
@receiver(m2m_changed, sender=Post.users_like.through)
def like_counter(sender, **kwargs):
    instance: Post = kwargs.get("instance", None)
    action = kwargs.get("action", None)
    if action == "post_add":
        instance.likes += 1
        instance.save()
    elif action == "post_remove":
        instance.likes -= 1
        instance.save()
