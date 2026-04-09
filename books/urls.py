from django.urls import path
from . import views

urlpatterns = [
    path("authors/", AuthorCreateView.as_view()),
    path("books/", BookCreateView.as_view()),
    path("books/top-sellers/", TopSellersView.as_view()),
    path("books/<str:isbn>/", BookByISBNView.as_view()),
    path("authors/<int:author_id>/books/", BooksByAuthorView.as_view()),
]
