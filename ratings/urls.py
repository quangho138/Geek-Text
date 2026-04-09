from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:book_id>/reviews/', views.create_review, name="create_review"),
    path('books/<int:book_id>/reviews/<int:review_id>', views.get_update_review, name="get_update_review"),
    path('books/<int:book_id>/reviews/avg', views.get_avg_rating, name="get_avg_rating"),
    path('ratings/', views.get_ratings, name='get_ratings')
]