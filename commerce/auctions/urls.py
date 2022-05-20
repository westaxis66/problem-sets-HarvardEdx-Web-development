from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name = "post"),
    path("listing/<int:listing_id>", views.listing, name = "listing"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("close/<int:listing_id>", views.close, name = "close"),
    path("closeditems", views.closeditems, name = "closeditems"),
    path("categories", views.categories, name = "categories"),
    path("listing/<str:category>", views.category_choices, name = "category_choices"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("delete_comment/<int:listing_id>", views.delete_comment, name="delete_comment"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("bidding/<int:listing_id>", views.bidding, name="bidding"),
    
]
