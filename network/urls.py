
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:followerid> to <int:userid>", views.follow, name="follow"),
    path("profile/<int:unfollowerid> to <int:userid>", views.unfollow, name="unfollow"),
    path("following", views.follow_sec, name="followsection"),
    path("like/<int:postid>", views.like, name="like"),
    path("unlike/<int:postid>", views.unlike, name="unlike"),
    path("edit/<int:post_id>", views.edit, name="edit"),

]
