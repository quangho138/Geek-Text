from django.urls import path
from .views import (
    AuthorCreateView,
    BookCreateView,
    BookByISBNView,
    BooksByAuthorView,
    TopSellersView,
)

urlpatterns = [
    path("books/top-sellers/", views.top_sellers, name="top_sellers"),
    path("books/genre/<str:genre>/", views.books_by_genre, name="books_by_genre"),
]
