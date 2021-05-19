from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create"),
    path("listingpage/<int:listing_id>", views.listing_page, name="lpage"),
    #path("listingpage/close/<int:listing_id>", views.listing_close, name="lclose"),
    path("listingpage/wclist/<int:listing_id>", views.listing_wl, name="lwl"),
    path("listingpage/comment/<int:listing_id>", views.listing_comments, name="lc"),
    path("watchlist", views.watch_list, name="wl"),
    path("category", views.categories, name="cat"),
    path("category/<int:category_id>", views.category_list, name="catl")

]
