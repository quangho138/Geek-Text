from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list),
    path('genre/', views.books_by_genre),
    path('top-sellers/', views.top_sellers),
    path('rating/', views.books_by_rating),
    path('discount/', views.discount_books),
]