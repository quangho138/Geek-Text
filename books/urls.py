from django.urls import path
from .views import (
    AuthorCreateView,
    BookCreateView,
    BookByISBNView,
    BooksByAuthorView,
    TopSellersView,
)

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/genre/<str:genre>/", views.books_by_genre, name="books_by_genre"),
    path("authors/", AuthorCreateView.as_view()),
    path("books/", BookCreateView.as_view()),
    path("books/top-sellers/", TopSellersView.as_view()),
    path("books/<str:isbn>/", BookByISBNView.as_view()),
    path("authors/<int:author_id>/books/", BooksByAuthorView.as_view()),
]

