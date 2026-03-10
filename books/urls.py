from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/genre/<str:genre>/", views.books_by_genre, name="books_by_genre"),
]

