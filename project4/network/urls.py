
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost", views.create_post, name="new_post"),
    path("allposts", views.all_posts, name="all_posts"),
    path("perfil/<str:perfil>", views.perfil, name="perfil"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    

    # API Routes
    path("editpost", views.edit_post, name="edit_post"),
    path("likes", views.likes, name="likes")
]
