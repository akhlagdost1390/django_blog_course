from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.category_list, name="categories_list"),
    path("categories/<slug:slug>/", views.category_posts, name="category_posts"),
    path("categories/<str:category>/<slug:slug>/", views.detail, name="detail"),
    path("categories/<str:category>/<slug:slug>/edit/", views.edit, name="edit"),
    path("categories/<str:category>/<slug:slug>/delete/", views.delete, name="delete"),

    path("like/", views.like, name="like"),
    path("new_post/", views.new_post, name="new_post"),
]
