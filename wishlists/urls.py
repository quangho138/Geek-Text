from django.urls import path
from .views import WishlistCreateView
from .views import AddBookToWishlistView

urlpatterns = [
    path("create/", WishlistCreateView.as_view(), name="wishlist-create"),
    path("add-book/", AddBookToWishlistView.as_view(), name="wishlist-add-book"),
]