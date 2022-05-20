from django.conf import settings
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("post/<str:post_id>", views.post, name="post"),
    path("post", views.post, name="post"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like/<int:id>", views.like, name="like"),
    path("delete/<str:post_id>", views.delete, name="delete"),
    

]
