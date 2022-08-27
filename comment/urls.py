from django.urls import path
from . import views

app_name = "comment"
urlpatterns = [path("send/", views.send, name="send")]
