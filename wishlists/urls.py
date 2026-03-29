from django.urls import path
from .views import WishlistCreateView
from .views import AddBookToWishlistView
from .views import RemoveBookFromWishlistView


urlpatterns = [
    path("create/", WishlistCreateView.as_view(), name="wishlist-create"),
    path("add-book/", AddBookToWishlistView.as_view(), name="wishlist-add-book"),
    path("<int:wishlist_id>/books/<int:book_id>/",
        RemoveBookFromWishlistView.as_view(),
        name="remove-book-from-wishlist",
    ),
]